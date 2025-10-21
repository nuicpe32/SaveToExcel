import api from './api';

export interface LineStatus {
  connected: boolean;
  line_display_name?: string;
  line_picture_url?: string;
  is_active?: boolean;
  linked_at?: string;
  notify_new_case?: boolean;
  notify_case_update?: boolean;
  notify_summons_sent?: boolean;
  notify_email_opened?: boolean;
}

export interface NotificationPreferences {
  notify_new_case?: boolean;
  notify_case_update?: boolean;
  notify_summons_sent?: boolean;
  notify_email_opened?: boolean;
}

export interface NotificationLog {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  status: string;
  error_message?: string;
  sent_at?: string;
  created_at?: string;
}

export const lineService = {
  async getAuthUrl(): Promise<string> {
    const response = await api.get('/line/auth-url');
    return response.data.auth_url;
  },

  async getStatus(): Promise<LineStatus> {
    const response = await api.get('/line/status');
    return response.data;
  },

  async updatePreferences(preferences: NotificationPreferences): Promise<void> {
    await api.put('/line/preferences', preferences);
  },

  async disconnect(): Promise<void> {
    await api.delete('/line/disconnect');
  },

  async sendTestNotification(): Promise<void> {
    await api.post('/line/test-notification', {});
  },

  async getNotificationHistory(limit: number = 50): Promise<NotificationLog[]> {
    const response = await api.get('/line/notification-history', {
      params: { limit },
    });
    return response.data.logs;
  },
};
