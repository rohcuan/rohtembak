import axios from 'axios'

const API_BASE_URL = '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('subscription_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Subscription Auth API
export const subscriptionApi = {
  login: (username: string, password: string) =>
    apiClient.post('/auth/login', { username, password }),
  refresh: () => apiClient.get('/auth/refresh'),
}

// XL Auth API
export const xlAuthApi = {
  requestOTP: (msisdn: string) =>
    apiClient.post('/xl/otp/request', { msisdn }),
  verifyOTP: (msisdn: string, otp: string) =>
    apiClient.post('/xl/otp/verify', { msisdn, otp }),
  getAccounts: () => apiClient.get('/xl/accounts'),
  switchAccount: (msisdn: string) =>
    apiClient.post('/xl/switch', { msisdn }),
  removeAccount: (msisdn: string) =>
    apiClient.delete(`/xl/accounts/${msisdn}`),
  getStatus: () => apiClient.get('/xl/status'),
}

// Profile API
export const profileApi = {
  getProfile: () => apiClient.get('/profile/'),
  getBalance: () => apiClient.get('/profile/balance'),
  getTiering: () => apiClient.get('/profile/tiering'),
  getDashboard: () => apiClient.get('/profile/dashboard'),
}

// Packages API
export const packagesApi = {
  getFamilies: () => apiClient.get('/packages/families'),
  getFamily: (code: string) => apiClient.get(`/packages/family/${code}`),
  getPackage: (code: string) => apiClient.get(`/packages/${code}`),
  getAddons: (code: string) => apiClient.get(`/packages/${code}/addons`),
  getMyPackages: () => apiClient.get('/packages/my/active'),
  getHotPackages: () => apiClient.get('/packages/hot/list'),
  getHotBundles: () => apiClient.get('/packages/hot/bundles'),
}

// Purchase API
export const purchaseApi = {
  buyWithBalance: (optionCode: string) =>
    apiClient.post('/purchase/balance', { option_code: optionCode }),
  buyWithQRIS: (optionCode: string, amount: number) =>
    apiClient.post('/purchase/qris', { option_code: optionCode, amount }),
  buyWithEWallet: (optionCode: string, phoneNumber: string) =>
    apiClient.post('/purchase/ewallet', { option_code: optionCode, phone_number: phoneNumber }),
  buyWithDecoy: (optionCode: string, decoyType: string) =>
    apiClient.post('/purchase/decoy', { option_code: optionCode, decoy_type: decoyType }),
}

// Circle API
export const circleApi = {
  getStatus: () => apiClient.get('/circle/status'),
  getMembers: () => apiClient.get('/circle/members'),
  inviteMember: (phoneNumber: string) =>
    apiClient.post('/circle/invite', { phone_number: phoneNumber }),
  removeMember: (phoneNumber: string) =>
    apiClient.post('/circle/remove', { phone_number: phoneNumber }),
  acceptInvitation: (invitationId: string) =>
    apiClient.post('/circle/accept', { invitation_id: invitationId }),
  createCircle: (name: string) =>
    apiClient.post('/circle/create', { name }),
  getBonus: () => apiClient.get('/circle/bonus'),
}

// Family API
export const familyApi = {
  getData: () => apiClient.get('/family/data'),
  validateMsisdn: (phoneNumber: string, nik: string) =>
    apiClient.post('/family/validate', { phone_number: phoneNumber, nik }),
  changeMember: (oldNumber: string, newNumber: string, nik: string) =>
    apiClient.post('/family/change-member', { old_number: oldNumber, new_number: newNumber, nik }),
  removeMember: (phoneNumber: string) =>
    apiClient.post('/family/remove-member', { phone_number: phoneNumber }),
  setQuotaLimit: (phoneNumber: string, quotaLimit: number) =>
    apiClient.post('/family/quota-limit', { phone_number: phoneNumber, quota_limit: quotaLimit }),
}

// Notifications API
export const notificationsApi = {
  getAll: () => apiClient.get('/notifications/'),
  getDetail: (id: string) => apiClient.get(`/notifications/${id}`),
}

// Transactions API
export const transactionsApi = {
  getAll: () => apiClient.get('/transactions/'),
}

export default apiClient
