/**
 * Dashboard JavaScript - Seguindo princípios SOLID e modularização
 * 
 * Módulos:
 * - ApiService: Responsável por todas as chamadas à API (SRP)
 * - DashboardManager: Gerencia o estado geral do dashboard (SRP)
 * - ConversationManager: Gerencia conversas ao vivo (SRP)
 * - ConfigurationManager: Gerencia configurações (SRP)
 * - StatisticsManager: Gerencia estatísticas (SRP)
 * - AppointmentManager: Gerencia consultas agendadas (SRP)
 */

// ===== API Service - Módulo para comunicação com backend =====
class ApiService {
    constructor() {
        this.baseUrl = '';
        this.headers = {
            'Content-Type': 'application/json'
        };
    }

    async request(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...this.headers,
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    // Métodos específicos da API
    async getStatistics() {
        return this.request('/estatisticas');
    }

    async getConfig() {
        return this.request('/config');
    }

    async getConversationHistory(userId) {
        return this.request(`/historico/${userId}`);
    }

    async getConversationStatus(userId) {
        return this.request(`/conversa/status/${userId}`);
    }

    async restartConversation(userId) {
        return this.request(`/conversa/reiniciar/${userId}`, {
            method: 'POST'
        });
    }

    async getAllAppointments() {
        return this.request('/consultas');
    }

    async getUserAppointments(userId) {
        return this.request(`/consultas/${userId}`);
    }

    async getHealthCheck() {
        return this.request('/health');
    }
}

// ===== Utilities =====
class Utils {
    static formatDate(dateString) {
        // Verifica se é uma data em formato brasileiro (DD/MM/YYYY)
        if (dateString && dateString.includes('/')) {
            const [day, month, year] = dateString.split('/');
            const date = new Date(year, month - 1, day);
            return date.toLocaleDateString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        }
        
        // Se for formato ISO ou outro formato
        if (dateString) {
            return new Date(dateString).toLocaleDateString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        return 'Data inválida';
    }

    static formatTime(dateString) {
        // Para período (manhã, tarde, noite), retorna o período
        if (dateString && (dateString.includes('manhã') || dateString.includes('tarde') || dateString.includes('noite'))) {
            return dateString;
        }
        
        // Se for um horário real
        if (dateString && dateString.includes('/')) {
            return 'Período não especificado';
        }
        
        return new Date(dateString).toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    static showToast(message, type = 'info') {
        // Implementação de toast notifications
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// ===== Statistics Manager =====
class StatisticsManager {
    constructor(apiService) {
        this.apiService = apiService;
        this.elements = {
            totalConsultas: document.getElementById('total-consultas'),
            usuariosUnicos: document.getElementById('usuarios-unicos'),
            consultasHoje: document.getElementById('consultas-hoje')
        };
    }

    async loadStatistics() {
        try {
            const stats = await this.apiService.getStatistics();
            this.updateStatistics(stats);
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
            Utils.showToast('Erro ao carregar estatísticas', 'danger');
        }
    }

    updateStatistics(stats) {
        this.elements.totalConsultas.textContent = stats.total_consultas || 0;
        this.elements.usuariosUnicos.textContent = stats.usuarios_unicos || 0;
        
        // Usar consultas criadas hoje (baseado no timestamp) ou consultas agendadas para hoje
        const consultasHoje = stats.consultas_criadas_hoje || stats.consultas_hoje || 0;
        this.elements.consultasHoje.textContent = consultasHoje;
    }

    startAutoRefresh() {
        setInterval(() => {
            this.loadStatistics();
        }, 30000); // Atualiza a cada 30 segundos
    }
}

// ===== Conversation Manager =====
class ConversationManager {
    constructor(apiService) {
        this.apiService = apiService;
        this.activeConversations = new Map();
        this.elements = {
            liveConversations: document.getElementById('live-conversations'),
            searchUser: document.getElementById('search-user'),
            btnSearch: document.getElementById('btn-search'),
            conversationHistory: document.getElementById('conversation-history'),
            modal: document.getElementById('conversationModal'),
            modalContent: document.getElementById('modal-conversation-content'),
            restartBtn: document.getElementById('restart-conversa')
        };
        this.currentUserId = null;
        this.initEventListeners();
    }

    initEventListeners() {
        this.elements.btnSearch.addEventListener('click', () => {
            this.searchConversation();
        });

        this.elements.searchUser.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchConversation();
            }
        });

        this.elements.restartBtn.addEventListener('click', () => {
            this.restartCurrentConversation();
        });
    }

    async searchConversation() {
        const userId = this.elements.searchUser.value.trim();
        if (!userId) {
            Utils.showToast('Digite um ID de usuário para buscar', 'warning');
            return;
        }

        try {
            this.elements.conversationHistory.innerHTML = '<div class="loading">Carregando...</div>';
            
            const history = await this.apiService.getConversationHistory(userId);
            this.displayConversationHistory(history, userId);
        } catch (error) {
            console.error('Erro ao buscar histórico:', error);
            this.elements.conversationHistory.innerHTML = `
                <div class="error-state">
                    <i class="bi bi-exclamation-triangle"></i>
                    <p>Erro ao carregar histórico</p>
                </div>
            `;
            Utils.showToast('Erro ao buscar histórico da conversa', 'danger');
        }
    }

    displayConversationHistory(history, userId) {
        if (!history || history.length === 0) {
            this.elements.conversationHistory.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-chat-square-text"></i>
                    <p>Nenhuma conversa encontrada para este usuário</p>
                </div>
            `;
            return;
        }

        const historyHtml = history.map((msg, index) => `
            <div class="conversation-item" onclick="conversationManager.showConversationDetails('${userId}')">
                <div class="d-flex justify-content-between">
                    <strong>${msg.remetente === 'user' ? '👤 Usuário' : '🤖 Bot'}</strong>
                    <span class="conversation-meta">${Utils.formatDate(msg.timestamp)}</span>
                </div>
                <div class="conversation-preview">${msg.mensagem || 'Mensagem vazia'}</div>
                ${msg.remetente === 'user' ? '<small class="text-primary">Enviada</small>' : '<small class="text-success">Resposta</small>'}
            </div>
        `).join('');

        this.elements.conversationHistory.innerHTML = historyHtml;
    }

    async showConversationDetails(userId) {
        this.currentUserId = userId;
        
        try {
            const [history, status] = await Promise.all([
                this.apiService.getConversationHistory(userId),
                this.apiService.getConversationStatus(userId)
            ]);

            this.displayConversationModal(history, status, userId);
            new bootstrap.Modal(this.elements.modal).show();
        } catch (error) {
            console.error('Erro ao carregar detalhes da conversa:', error);
            Utils.showToast('Erro ao carregar detalhes da conversa', 'danger');
        }
    }

    displayConversationModal(history, status, userId) {
        const statusBadge = `<span class="badge bg-primary">${status.estado}</span>`;
        
        const messagesHtml = history.map(msg => `
            <div class="chat-message ${msg.remetente === 'user' ? 'user' : 'bot'}">
                <div>${msg.mensagem}</div>
                <div class="chat-timestamp">${Utils.formatDate(msg.timestamp)}</div>
            </div>
        `).join('');

        this.elements.modalContent.innerHTML = `
            <div class="mb-3">
                <h6>Usuário: ${userId}</h6>
                <p>Status: ${statusBadge}</p>
            </div>
            <div class="conversation-messages" style="max-height: 400px; overflow-y: auto;">
                ${messagesHtml}
            </div>
        `;
    }

    async restartCurrentConversation() {
        if (!this.currentUserId) return;

        try {
            await this.apiService.restartConversation(this.currentUserId);
            Utils.showToast('Conversa reiniciada com sucesso', 'success');
            bootstrap.Modal.getInstance(this.elements.modal).hide();
            this.searchConversation(); // Recarrega o histórico
        } catch (error) {
            console.error('Erro ao reiniciar conversa:', error);
            Utils.showToast('Erro ao reiniciar conversa', 'danger');
        }
    }

    updateLiveConversations(conversations) {
        // Placeholder para conversas ao vivo (implementar WebSocket futuramente)
        this.elements.liveConversations.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-chat-dots pulse"></i>
                <p>Monitoramento em tempo real será implementado com WebSocket</p>
            </div>
        `;
    }
}

// ===== Configuration Manager =====
class ConfigurationManager {
    constructor(apiService) {
        this.apiService = apiService;
        this.elements = {
            configForm: document.getElementById('config-form'),
            twilioSid: document.getElementById('twilio-sid'),
            twilioToken: document.getElementById('twilio-token'),
            whatsappNumber: document.getElementById('whatsapp-number')
        };
        this.initEventListeners();
        this.loadCurrentConfig();
    }

    initEventListeners() {
        this.elements.configForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveConfiguration();
        });
    }

    async loadCurrentConfig() {
        try {
            // Carrega configurações do backend (.env)
            const config = await this.apiService.getConfig();
            
            this.elements.twilioSid.value = config.twilio_sid || '';
            this.elements.whatsappNumber.value = config.whatsapp_number || '';
            
            // Indica se há token configurado (sem mostrá-lo)
            if (config.has_token) {
                this.elements.twilioToken.placeholder = 'Token configurado (oculto por segurança)';
            } else {
                this.elements.twilioToken.placeholder = 'Token não configurado';
            }
            
        } catch (error) {
            console.error('Erro ao carregar configurações:', error);
            // Fallback para localStorage se a API falhar
            this.elements.twilioSid.value = localStorage.getItem('twilio_sid') || '';
            this.elements.whatsappNumber.value = localStorage.getItem('whatsapp_number') || '';
            Utils.showToast('Carregadas configurações locais (offline)', 'warning');
        }
    }

    saveConfiguration() {
        const config = {
            twilioSid: this.elements.twilioSid.value,
            twilioToken: this.elements.twilioToken.value,
            whatsappNumber: this.elements.whatsappNumber.value
        };

        // Salva no localStorage (em produção, enviar para backend)
        localStorage.setItem('twilio_sid', config.twilioSid);
        localStorage.setItem('whatsapp_number', config.whatsappNumber);

        Utils.showToast('⚠️ Configurações salvas localmente. Para aplicar no servidor, edite o arquivo .env e reinicie a aplicação.', 'warning');

        // Limpa o token por segurança
        this.elements.twilioToken.value = '';
    }
}

// ===== Appointment Manager =====
class AppointmentManager {
    constructor(apiService) {
        this.apiService = apiService;
        this.elements = {
            scheduledAppointments: document.getElementById('scheduled-appointments'),
            filterPeriod: document.getElementById('filter-period'),
            refreshBtn: document.getElementById('refresh-consultas')
        };
        this.appointments = [];
        this.initEventListeners();
    }

    initEventListeners() {
        this.elements.filterPeriod.addEventListener('change', () => {
            this.filterAppointments();
        });

        this.elements.refreshBtn.addEventListener('click', () => {
            this.loadAppointments();
        });
    }

    async loadAppointments() {
        try {
            this.elements.scheduledAppointments.innerHTML = '<div class="loading">Carregando consultas...</div>';
            
            this.appointments = await this.apiService.getAllAppointments();
            this.filterAppointments();
        } catch (error) {
            console.error('Erro ao carregar consultas:', error);
            this.elements.scheduledAppointments.innerHTML = `
                <div class="error-state">
                    <i class="bi bi-exclamation-triangle"></i>
                    <p>Erro ao carregar consultas</p>
                </div>
            `;
            Utils.showToast('Erro ao carregar consultas agendadas', 'danger');
        }
    }

    filterAppointments() {
        const filter = this.elements.filterPeriod.value;
        const now = new Date();
        
        let filteredAppointments = this.appointments;

        switch (filter) {
            case 'today':
                const today = new Date().toLocaleDateString('pt-BR').split('/').reverse().join('-');
                filteredAppointments = this.appointments.filter(apt => {
                    if (apt.data && apt.data.includes('/')) {
                        const [day, month, year] = apt.data.split('/');
                        const aptDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
                        return aptDate === today;
                    }
                    return false;
                });
                break;
            case 'week':
                const weekAgo = new Date();
                weekAgo.setDate(weekAgo.getDate() - 7);
                filteredAppointments = this.appointments.filter(apt => {
                    if (apt.data && apt.data.includes('/')) {
                        const [day, month, year] = apt.data.split('/');
                        const aptDate = new Date(year, month - 1, day);
                        return aptDate >= weekAgo;
                    }
                    return false;
                });
                break;
            case 'month':
                const monthAgo = new Date();
                monthAgo.setMonth(monthAgo.getMonth() - 1);
                filteredAppointments = this.appointments.filter(apt => {
                    if (apt.data && apt.data.includes('/')) {
                        const [day, month, year] = apt.data.split('/');
                        const aptDate = new Date(year, month - 1, day);
                        return aptDate >= monthAgo;
                    }
                    return false;
                });
                break;
        }

        this.displayAppointments(filteredAppointments);
    }

    displayAppointments(appointments) {
        if (!appointments || appointments.length === 0) {
            this.elements.scheduledAppointments.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-calendar-x"></i>
                    <p>Nenhuma consulta encontrada</p>
                </div>
            `;
            return;
        }

        const appointmentsHtml = appointments.map(apt => `
            <div class="appointment-item fade-in">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <div class="appointment-date">${Utils.formatDate(apt.data)}</div>
                        <div class="appointment-time">${Utils.formatTime(apt.periodo)}</div>
                        <div class="appointment-user">
                            <strong>${apt.nome}</strong> - Usuário: ${apt.user_id}
                        </div>
                        <small class="text-muted">Criado em: ${Utils.formatDate(apt.data_criacao)}</small>
                    </div>
                    <span class="appointment-status status-confirmed">Confirmada</span>
                </div>
            </div>
        `).join('');

        this.elements.scheduledAppointments.innerHTML = appointmentsHtml;
    }
}

// ===== Dashboard Manager - Classe principal =====
class DashboardManager {
    constructor() {
        this.apiService = new ApiService();
        this.statisticsManager = new StatisticsManager(this.apiService);
        this.conversationManager = new ConversationManager(this.apiService);
        this.configurationManager = new ConfigurationManager(this.apiService);
        this.appointmentManager = new AppointmentManager(this.apiService);
        
        this.init();
    }

    async init() {
        try {
            // Verifica se o sistema está online
            await this.apiService.getHealthCheck();
            
            // Carrega dados iniciais
            await Promise.all([
                this.statisticsManager.loadStatistics(),
                this.appointmentManager.loadAppointments()
            ]);

            // Inicia atualizações automáticas
            this.statisticsManager.startAutoRefresh();

            Utils.showToast('Dashboard carregado com sucesso!', 'success');
        } catch (error) {
            console.error('Erro ao inicializar dashboard:', error);
            Utils.showToast('Erro ao conectar com o servidor', 'danger');
        }
    }
}

// ===== Inicialização =====
document.addEventListener('DOMContentLoaded', () => {
    // Inicializa o dashboard
    window.dashboardManager = new DashboardManager();
    window.conversationManager = dashboardManager.conversationManager;
    
    // Tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});