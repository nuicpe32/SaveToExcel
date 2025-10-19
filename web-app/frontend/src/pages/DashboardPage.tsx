import { useCallback, useEffect, useState } from 'react'
import { Table, message, Tag, Space, Button, Descriptions, Drawer, Tabs, Popconfirm, Modal, Input, Upload, Card, List, Spin } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { EditOutlined, DeleteOutlined, PlusOutlined, PrinterOutlined, UploadOutlined, FileExcelOutlined, ApartmentOutlined, MailOutlined, HistoryOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { useAuthStore } from '../stores/authStore'
import BankAccountFormModal from '../components/BankAccountFormModal'
import NonBankAccountFormModal from '../components/NonBankAccountFormModal'
import PaymentGatewayAccountFormModal from '../components/PaymentGatewayAccountFormModal'
import TelcoMobileAccountFormModal from '../components/TelcoMobileAccountFormModal'
import TelcoInternetAccountFormModal from '../components/TelcoInternetAccountFormModal'
import SuspectFormModal from '../components/SuspectFormModal'
import EmailConfirmationModal from '../components/EmailConfirmationModal'
import EmailHistoryModal from '../components/EmailHistoryModal'
import CfrFlowChart from '../components/CfrFlowChart'
import dayjs from 'dayjs'

interface BankAccount {
  id: number
  order_number?: number
  document_number?: string
  document_date?: string
  document_date_thai?: string
  bank_name: string
  account_number: string
  account_name: string
  account_owner?: string
  complainant?: string
  victim_name?: string
  case_id?: string
  time_period?: string
  delivery_date?: string
  delivery_month?: string
  delivery_time?: string
  reply_status: boolean
  status: string
  // Note: bank_branch and bank_address removed - use headquarters address from banks table
}

interface NonBankAccount {
  id: number
  non_bank_id?: number
  document_number?: string
  document_date?: string
  account_number: string
  account_name: string
  time_period?: string
  delivery_date?: string
  reply_status: boolean
  status: string
  // Virtual fields from backend
  provider_name?: string
}

interface PaymentGatewayAccount {
  id: number
  payment_gateway_id?: number
  bank_id?: number
  document_number?: string
  document_date?: string
  account_number: string
  account_name: string
  time_period?: string
  delivery_date?: string
  reply_status: boolean
  status: string
  // Virtual fields from backend
  provider_name?: string
  bank_name?: string
}

interface TelcoMobileAccount {
  id: number
  telco_mobile_id?: number
  document_number?: string
  document_date?: string
  provider_name: string  // ชื่อผู้ให้บริการ
  phone_number: string   // หมายเลขโทรศัพท์
  time_period?: string
  delivery_date?: string
  reply_status: boolean
  status: string
}

interface TelcoInternetAccount {
  id: number
  telco_internet_id?: number
  document_number?: string
  document_date?: string
  provider_name: string  // ชื่อผู้ให้บริการ
  ip_address: string     // IP Address
  time_period?: string
  delivery_date?: string
  reply_status: boolean
  status: string
}

interface Suspect {
  id: number
  document_number?: string
  document_date?: string
  document_date_thai?: string
  suspect_name: string
  suspect_id_card?: string
  suspect_address?: string
  police_station?: string
  police_province?: string
  police_address?: string
  complainant?: string
  victim_name?: string
  case_id?: string
  appointment_date?: string
  appointment_date_thai?: string
  reply_status: boolean
  status: string
}

interface CriminalCase {
  id: number
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  case_type?: string
  complaint_date?: string
  complaint_date_thai?: string
  incident_date?: string
  incident_date_thai?: string
  damage_amount?: string
  case_age_months?: number
  case_age_days?: number
  bank_accounts_count?: string
  suspects_count?: string
  court_name?: string
  row_class?: string
  row_style?: Record<string, any>
}

export default function DashboardPage() {
  const [data, setData] = useState<CriminalCase[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const [selected, setSelected] = useState<CriminalCase | null>(null)
  const [bankAccounts, setBankAccounts] = useState<BankAccount[]>([])
  const [nonBankAccounts, setNonBankAccounts] = useState<NonBankAccount[]>([])
  const [paymentGatewayAccounts, setPaymentGatewayAccounts] = useState<PaymentGatewayAccount[]>([])
  const [telcoMobileAccounts, setTelcoMobileAccounts] = useState<TelcoMobileAccount[]>([])
  const [telcoInternetAccounts, setTelcoInternetAccounts] = useState<TelcoInternetAccount[]>([])
  const [suspects, setSuspects] = useState<Suspect[]>([])
  const [loadingDetails, setLoadingDetails] = useState(false)
  const [suspectDetailOpen, setSuspectDetailOpen] = useState(false)
  const [selectedSuspect, setSelectedSuspect] = useState<Suspect | null>(null)
  const [bankModalVisible, setBankModalVisible] = useState(false)
  const [paymentGatewayModalVisible, setPaymentGatewayModalVisible] = useState(false)
  const [telcoMobileModalVisible, setTelcoMobileModalVisible] = useState(false)
  const [telcoInternetModalVisible, setTelcoInternetModalVisible] = useState(false)
  const [suspectModalVisible, setSuspectModalVisible] = useState(false)
  const [editingBank, setEditingBank] = useState<BankAccount | null>(null)
  const [editingNonBank, setEditingNonBank] = useState<NonBankAccount | null>(null)
  const [editingPaymentGateway, setEditingPaymentGateway] = useState<PaymentGatewayAccount | null>(null)
  const [editingTelcoMobile, setEditingTelcoMobile] = useState<TelcoMobileAccount | null>(null)
  const [editingTelcoInternet, setEditingTelcoInternet] = useState<TelcoInternetAccount | null>(null)
  const [nonBankModalVisible, setNonBankModalVisible] = useState(false)
  const [editingSuspect, setEditingSuspect] = useState<Suspect | null>(null)
  const [cfrFiles, setCfrFiles] = useState<any[]>([])
  const [uploadingCfr, setUploadingCfr] = useState(false)
  const [cfrRecords, setCfrRecords] = useState<any[]>([])
  const [loadingCfr, setLoadingCfr] = useState(false)
  const [selectedCfrAccount, setSelectedCfrAccount] = useState<any>(null)
  const [cfrDetailVisible, setCfrDetailVisible] = useState(false)
  const [flowChartVisible, setFlowChartVisible] = useState(false)

  // Email Modal States
  const [emailModalVisible, setEmailModalVisible] = useState(false)
  const [emailAccountType, setEmailAccountType] = useState<'non_bank' | 'payment_gateway' | 'telco_mobile' | 'telco_internet' | 'bank'>('non_bank')
  const [emailAccountId, setEmailAccountId] = useState<number>(0)
  const [emailProviderName, setEmailProviderName] = useState<string>('')
  const [emailDocumentNumber, setEmailDocumentNumber] = useState<string>('')
  const [emailDefaultEmail, setEmailDefaultEmail] = useState<string>('')
  const [emailAccountNumber, setEmailAccountNumber] = useState<string>('')
  const [emailPhoneNumber, setEmailPhoneNumber] = useState<string>('')
  const [emailIpAddress, setEmailIpAddress] = useState<string>('')

  // Email History Modal States
  const [emailHistoryVisible, setEmailHistoryVisible] = useState(false)
  const [historyAccountType, setHistoryAccountType] = useState<'non_bank' | 'payment_gateway' | 'telco_mobile' | 'telco_internet' | 'bank'>('non_bank')
  const [historyAccountId, setHistoryAccountId] = useState<number>(0)
  const [historyAccountInfo, setHistoryAccountInfo] = useState<{
    documentNumber?: string;
    providerName?: string;
    accountNumber?: string;
  }>({})

  // Handler สำหรับเปิด Email History Modal
  const handleShowEmailHistory = (
    accountType: 'non_bank' | 'payment_gateway' | 'telco_mobile' | 'telco_internet' | 'bank',
    accountId: number,
    accountInfo: { documentNumber?: string; providerName?: string; accountNumber?: string }
  ) => {
    setHistoryAccountType(accountType)
    setHistoryAccountId(accountId)
    setHistoryAccountInfo(accountInfo)
    setEmailHistoryVisible(true)
  }

  // ฟังก์ชันแปลงวันที่เป็นรูปแบบไทย
  const formatThaiDate = (date: string | undefined): string => {
    if (!date) return '-'
    
    const thaiMonths = [
      'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
      'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
    ]
    
    const dayjsDate = dayjs(date)
    const day = dayjsDate.date()
    const month = thaiMonths[dayjsDate.month()]
    const year = dayjsDate.year() + 543 // แปลงเป็น พ.ศ.
    
    return `${day} ${month} ${year}`
  }
  
  // Statistics state
  const [stats, setStats] = useState({
    totalCases: 0,
    processingCases: 0,
    over6MonthsCases: 0,
    closedCases: 0
  })
  
  const navigate = useNavigate()
  const { token, user } = useAuthStore()

  // คำนวณสถิติจากข้อมูลคดี
  const calculateStats = useCallback((cases: CriminalCase[]) => {
    const now = new Date()
    const sixMonthsAgo = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate())
    
    const totalCases = cases.length
    let processingCases = 0
    let over6MonthsCases = 0
    let closedCases = 0
    
    cases.forEach(caseItem => {
      // ตรวจสอบสถานะคดี - มีแค่ 2 สถานะ: 'จำหน่าย' และ 'ระหว่างสอบสวน'
      if (caseItem.status === 'จำหน่าย') {
        closedCases++
      } else if (caseItem.status === 'ระหว่างสอบสวน') {
        processingCases++
        
        // ตรวจสอบคดีที่เกิน 6 เดือน (เฉพาะคดีที่ยังดำเนินการอยู่)
        if (caseItem.complaint_date) {
          const complaintDate = new Date(caseItem.complaint_date)
          if (complaintDate < sixMonthsAgo) {
            over6MonthsCases++
          }
        }
      }
    })
    
    console.log('📊 Statistics calculation:', {
      totalCases,
      processingCases,
      over6MonthsCases,
      closedCases,
      statusBreakdown: cases.reduce((acc, caseItem) => {
        acc[caseItem.status] = (acc[caseItem.status] || 0) + 1
        return acc
      }, {} as Record<string, number>)
    })
    
    return {
      totalCases,
      processingCases,
      over6MonthsCases,
      closedCases
    }
  }, [])

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      console.log('🔍 Dashboard: Fetching data...', { token: !!token, user: !!user })
      
      const res = await api.get<CriminalCase[]>('/criminal-cases/')
      console.log('📊 Dashboard: Data received:', res.data.length, 'cases')
      
      // Sort by complaint_date descending (newest first)
      const sortedData = res.data.sort((a, b) => {
        if (!a.complaint_date && !b.complaint_date) return 0
        if (!a.complaint_date) return 1
        if (!b.complaint_date) return -1
        return new Date(b.complaint_date).getTime() - new Date(a.complaint_date).getTime()
      })
      setData(sortedData)
      
      // คำนวณสถิติ
      const calculatedStats = calculateStats(sortedData)
      setStats(calculatedStats)
      
      console.log('✅ Dashboard: Data sorted and set:', sortedData.length, 'cases')
      console.log('📊 Dashboard: Statistics calculated:', calculatedStats)
    } catch (err: any) {
      console.error('❌ Dashboard: Error fetching data:', err)
      console.error('❌ Dashboard: Error response:', err.response?.data)
      console.error('❌ Dashboard: Error status:', err.response?.status)
      message.error('ไม่สามารถดึงข้อมูลคดีอาญาได้')
    } finally {
      setLoading(false)
    }
  }, [token, user])

  useEffect(() => {
    console.log('🚀 Dashboard: Component mounted, token:', !!token, 'user:', !!user)
    if (!token || !user) {
      console.log('⚠️ Dashboard: No auth token or user, redirecting to login')
      navigate('/login')
      return
    }
    fetchData()
  }, [fetchData, navigate, token, user])

  const fetchCaseDetails = useCallback(async (caseId: number) => {
    try {
      setLoadingDetails(true)
      const [bankRes, nonBankRes, paymentGatewayRes, telcoMobileRes, telcoInternetRes, suspectsRes] = await Promise.all([
        api.get<BankAccount[]>(`/criminal-cases/${caseId}/bank-accounts`),
        api.get<NonBankAccount[]>(`/non-bank-accounts/by-case/${caseId}`),
        api.get<PaymentGatewayAccount[]>(`/payment-gateway-accounts/by-case/${caseId}`),
        api.get<TelcoMobileAccount[]>(`/telco-mobile-accounts/by-case/${caseId}`),
        api.get<TelcoInternetAccount[]>(`/telco-internet-accounts/by-case/${caseId}`),
        api.get<Suspect[]>(`/criminal-cases/${caseId}/suspects`)
      ])
      setBankAccounts(bankRes.data)
      setNonBankAccounts(nonBankRes.data)
      setPaymentGatewayAccounts(paymentGatewayRes.data)
      setTelcoMobileAccounts(telcoMobileRes.data)
      setTelcoInternetAccounts(telcoInternetRes.data)
      setSuspects(suspectsRes.data)
    } catch (err) {
      message.error('ไม่สามารถดึงข้อมูลรายละเอียดคดีได้')
    } finally {
      setLoadingDetails(false)
    }
  }, [])

  const showDetails = (record: CriminalCase) => {
    setSelected(record)
    setOpen(true)
    fetchCaseDetails(record.id)
    fetchCfrFiles(record.id)
  }

  const fetchCfrFiles = async (caseId: number) => {
    try {
      const response = await api.get(`/cfr/${caseId}/files`)
      setCfrFiles(response.data)
      // โหลดข้อมูล records ด้วย
      fetchCfrRecords(caseId)
    } catch (error) {
      console.error('ไม่สามารถโหลดข้อมูลไฟล์ CFR ได้')
    }
  }

  const fetchCfrRecords = async (caseId: number) => {
    setLoadingCfr(true)
    try {
      const response = await api.get(`/cfr/${caseId}/records`, {
        params: { limit: 1000 } // โหลดสูงสุด 1000 records
      })
      setCfrRecords(response.data.records || [])
    } catch (error) {
      console.error('ไม่สามารถโหลดข้อมูล CFR records ได้')
      setCfrRecords([])
    } finally {
      setLoadingCfr(false)
    }
  }

  const showCfrAccountDetail = (record: any) => {
    setSelectedCfrAccount(record)
    setCfrDetailVisible(true)
  }

  // ฟังก์ชันสร้างหมายเรียกจากข้อมูล CFR
  const handleCreateSummonsFromCfr = (cfrRecord: any) => {
    // Parse วันที่จาก CFR
    // ถ้าปีมากกว่า 2500 แสดงว่าเป็นปี พ.ศ. ต้องแปลงเป็น ค.ศ. ก่อน
    let transferDateStr = cfrRecord.transfer_date
    const year = parseInt(transferDateStr.split('-')[0])
    
    if (year > 2500) {
      // แปลงจาก พ.ศ. เป็น ค.ศ.
      const adYear = year - 543
      transferDateStr = transferDateStr.replace(year.toString(), adYear.toString())
    }
    
    // คำนวณช่วงเวลาทำธุรกรรม (1 วันก่อน - 1 วันหลัง)
    const transferDate = dayjs(transferDateStr)
    const startDate = transferDate.subtract(1, 'day')
    const endDate = transferDate.add(1, 'day')

    // หาธนาคารจาก bank_short_name
    const bankName = cfrRecord.to_bank_short_name
    let selectedBankName = ''
    
    // สร้าง mapping ของ bank_short_name กับ bank_name
    if (bankName) {
      const bankMapping: { [key: string]: string } = {
        'BBL': 'ธนาคารกรุงเทพ',
        'KBANK': 'ธนาคารกสิกรไทย',
        'KBNK': 'ธนาคารกสิกรไทย',  // เพิ่ม KBNK (รูปแบบอื่นของกสิกร)
        'KTB': 'ธนาคารกรุงไทย',
        'TTB': 'ธนาคารทหารไทยธนชาต',
        'SCB': 'ธนาคารไทยพาณิชย์',
        'BAY': 'ธนาคารกรุงศรีอยุธยา',
        'CIMBT': 'ธนาคารซีไอเอ็มบี ไทย',
        'UOBT': 'ธนาคารยูโอบี',
        'KKP': 'ธนาคารเกียรตินาคินภัทร',
        'GSB': 'ธนาคารออมสิน',
        'GHB': 'ธนาคารอาคารสงเคราะห์',
        'BAAC': 'ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร',
        'LH': 'ธนาคารแลนด์ แอนด์ เฮ้าส์'
      }
      
      selectedBankName = bankMapping[bankName] || bankName
    }

    // แปลงเดือนเป็นภาษาไทยแบบย่อ
    const formatThaiMonth = (month: number): string => {
      const thaiMonths = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 
                          'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
      return thaiMonths[month]
    }

    // แปลง date range เป็น text ไทย
    const formatDateRangeToThai = (start: dayjs.Dayjs, end: dayjs.Dayjs): string => {
      // แปลงเป็น พ.ศ.
      const startDay = start.date()
      const startMonth = formatThaiMonth(start.month())
      const startYear = (start.year() + 543).toString().slice(-2) // เอา 2 หลักหลัง
      
      const endDay = end.date()
      const endMonth = formatThaiMonth(end.month())
      const endYear = (end.year() + 543).toString().slice(-2)
      
      return `${startDay} ${startMonth} ${startYear} - ${endDay} ${endMonth} ${endYear}`
    }

    // สร้างข้อมูลสำหรับฟอร์ม
    const bankFormData = {
      bank_name: selectedBankName,
      account_number: cfrRecord.to_account_no || '',
      account_name: cfrRecord.to_account_name || '',
      // กรอก time_period โดยคำนวณจากวันที่ทำธุรกรรม (1 วันก่อน - 1 วันหลัง)
      time_period: formatDateRangeToThai(startDate, endDate),
      document_date: dayjs(), // วันที่ลงวันที่ = วันนี้
      delivery_date: dayjs().add(14, 'day'), // กำหนดส่ง = วันนี้ + 14 วัน
      is_frozen: false,
      // เพิ่มข้อมูลสำหรับ date range
      _date_range_start: startDate,
      _date_range_end: endDate,
      // Flag พิเศษเพื่อบอกว่านี่เป็นการสร้างใหม่ไม่ใช่การแก้ไข
      _is_new_from_cfr: true
    }

    // เปิดฟอร์มสร้างหมายเรียกพร้อมข้อมูลที่กรอกไว้
    setEditingBank(bankFormData as any)
    setBankModalVisible(true)
  }

  // ฟังก์ชันตรวจสอบว่าบัญชีมีในรายการหมายเรียกหรือไม่
  const findBankAccountSummons = (accountNo: string) => {
    if (!accountNo || !bankAccounts) return null
    
    // ลบช่องว่างและ - ออก
    const cleanAccountNo = accountNo.replace(/[\s-]/g, '')
    
    return bankAccounts.find(ba => {
      if (!ba.account_number) return false
      const cleanBankAccount = ba.account_number.replace(/[\s-]/g, '')
      return cleanBankAccount === cleanAccountNo
    })
  }

  // ฟังก์ชันแปลง bank_name เป็น bank_short_name สำหรับ logo
  const getNonBankShortName = (providerName: string): string => {
    if (!providerName) return ''
    
    const nonBankNameMap: { [key: string]: string } = {
      'บริษัท โอมิเซะ จำกัด': 'Omise',
      'โอมิเซะ': 'Omise',
      'Omise': 'Omise',
      'บริษัท โกลบอล ไพร์ม คอร์ปอเรชั่น จำกัด': 'GB',
      'GB Prime Pay': 'GB',
      'บริษัท ทูซีทูพี (ประเทศไทย) จำกัด': '2C2P',
      '2C2P': '2C2P',
      'บริษัท ทรู มันนี่ จำกัด': 'TrueMoney',
      'ทรู มันนี่': 'TrueMoney',
      'TrueMoney': 'TrueMoney',
    }
    
    // หาจากชื่อเต็ม
    if (nonBankNameMap[providerName]) {
      return nonBankNameMap[providerName]
    }
    
    // หาจากคำบางส่วน
    for (const [fullName, shortName] of Object.entries(nonBankNameMap)) {
      if (providerName.includes(fullName) || fullName.includes(providerName)) {
        return shortName
      }
    }
    
    return ''
  }

  const getBankShortName = (bankName: string): string => {
    if (!bankName) return ''
    
    const bankNameMap: { [key: string]: string } = {
      'ธนาคารกรุงเทพ': 'BBL',
      'ธนาคารกสิกรไทย': 'KBANK',
      'ธนาคารกรุงไทย': 'KTB',
      'ธนาคารทหารไทยธนชาต': 'TTB',
      'ธนาคารไทยพาณิชย์': 'SCB',
      'ธนาคารกรุงศรีอยุธยา': 'BAY',
      'ธนาคารซีไอเอ็มบี ไทย': 'CIMBT',
      'ธนาคารซีไอเอ็มบีไทย': 'CIMBT',
      'ธนาคารยูโอบี': 'UOBT',
      'ธนาคารเกียรตินาคินภัทร': 'KKP',
      'ธนาคารออมสิน': 'GSB',
      'ธนาคารอาคารสงเคราะห์': 'GHB',
      'ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร': 'BAAC',
      'ธนาคารแลนด์ แอนด์ เฮ้าส์': 'LH',
      'ธนาคารทิสโก้': 'TISCO',
      'ธนาคารธนชาต': 'TCRB',
      'ธนาคารไอซีบีซี (ไทย)': 'ICBC',
      'ธนาคารอิสลามแห่งประเทศไทย': 'IBANK'
    }
    
    // หาจากชื่อเต็ม
    if (bankNameMap[bankName]) {
      return bankNameMap[bankName]
    }
    
    // หาจากคำบางส่วน
    for (const [fullName, shortName] of Object.entries(bankNameMap)) {
      if (bankName.includes(fullName) || fullName.includes(bankName)) {
        return shortName
      }
    }
    
    return ''
  }

  // ฟังก์ชันคำนวณครั้งที่ผู้เสียหายโอน
  const getVictimTransferSequence = (currentRecord: any, allRecords: any[]): number | null => {
    if (!currentRecord || !allRecords || !selected?.complainant) return null
    
    // ตรวจสอบว่า record นี้เป็นการโอนของผู้เสียหายหรือไม่
    const isCurrentVictim = isVictimAccount(currentRecord.from_account_name)
    if (!isCurrentVictim) return null
    
    // หาธุรกรรมทั้งหมดที่ผู้เสียหายโอนออก
    const victimTransfers = allRecords.filter(record => {
      return isVictimAccount(record.from_account_name)
    })
    
    // เรียงตามวันเวลา (เก่าสุดไปใหม่สุด)
    const sortedTransfers = victimTransfers.sort((a, b) => {
      const dateTimeA = `${a.transfer_date} ${a.transfer_time || '00:00:00'}`
      const dateTimeB = `${b.transfer_date} ${b.transfer_time || '00:00:00'}`
      return dateTimeA.localeCompare(dateTimeB)
    })
    
    // หาลำดับของ record นี้
    const index = sortedTransfers.findIndex(t => 
      t.transfer_date === currentRecord.transfer_date &&
      t.transfer_time === currentRecord.transfer_time &&
      t.to_account_no === currentRecord.to_account_no &&
      t.transfer_amount === currentRecord.transfer_amount
    )
    
    return index >= 0 ? index + 1 : null
  }

  // ฟังก์ชันตรวจสอบว่าชื่อบัญชีตรงกับผู้เสียหายหรือไม่
  const isVictimAccount = (accountName: string): boolean => {
    if (!accountName || !selected?.complainant) return false
    
    const complainant = selected.complainant.trim()
    const account = accountName.trim()
    
    // ลบคำนำหน้า (นาย, นาง, นางสาว, น.ส., Mr., Mrs., Miss)
    const removeTitle = (name: string): string => {
      return name
        .replace(/^(นาย|นาง|นางสาว|น\.ส\.|Mr\.|Mrs\.|Miss|Ms\.)\s*/gi, '')
        .trim()
    }
    
    const cleanComplainant = removeTitle(complainant)
    const cleanAccount = removeTitle(account)
    
    // ตรวจสอบแบบต่างๆ
    // 1. ตรงกันทุกตัวอักษร
    if (cleanAccount === cleanComplainant) return true
    
    // 2. ตรงกันโดยไม่สนใจตัวพิมพ์ใหญ่/เล็ก
    if (cleanAccount.toLowerCase() === cleanComplainant.toLowerCase()) return true
    
    // 3. ตรงกันโดยไม่สนใจช่องว่าง
    if (cleanAccount.replace(/\s+/g, '') === cleanComplainant.replace(/\s+/g, '')) return true
    
    // 4. ผู้เสียหายเป็นส่วนหนึ่งของชื่อบัญชี
    if (cleanAccount.includes(cleanComplainant)) return true
    
    // 5. ชื่อบัญชีเป็นส่วนหนึ่งของผู้เสียหาย
    if (cleanComplainant.includes(cleanAccount)) return true
    
    // 6. ตรวจสอบแบบ fuzzy (คำแรกและคำสุดท้ายตรงกัน)
    const complainantWords = cleanComplainant.split(/\s+/).filter(w => w.length > 0)
    const accountWords = cleanAccount.split(/\s+/).filter(w => w.length > 0)
    
    if (complainantWords.length >= 2 && accountWords.length >= 2) {
      const firstMatch = complainantWords[0] === accountWords[0]
      const lastMatch = complainantWords[complainantWords.length - 1] === accountWords[accountWords.length - 1]
      if (firstMatch && lastMatch) return true
    }
    
    return false
  }

  const handleCfrUpload = async (file: File) => {
    if (!selected) return false
    
    setUploadingCfr(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post(`/cfr/upload/${selected.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      message.success(`${response.data.message} (เพิ่ม ${response.data.records_inserted} รายการ)`)
      fetchCfrFiles(selected.id)
      fetchCfrRecords(selected.id)
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'ไม่สามารถอัพโหลดไฟล์ได้')
    } finally {
      setUploadingCfr(false)
    }
    return false
  }

  const handleDeleteCfrFile = async (filename: string) => {
    if (!selected) return
    
    try {
      await api.delete(`/cfr/${selected.id}/file/${encodeURIComponent(filename)}`)
      message.success('ลบไฟล์ CFR สำเร็จ')
      fetchCfrFiles(selected.id)
      fetchCfrRecords(selected.id)
    } catch (error) {
      message.error('ไม่สามารถลบไฟล์ได้')
    }
  }

  const showSuspectDetail = (suspect: Suspect) => {
    setSelectedSuspect(suspect)
    setSuspectDetailOpen(true)
  }

  const handleEdit = (record: CriminalCase) => {
    navigate(`/edit-criminal-case/${record.id}`)
  }

  const handlePrintCaseReport = async (record: CriminalCase) => {
    try {
      // ดึงข้อมูล HTML จาก API (ใช้ api client ที่มี token)
      const response = await api.get(`/documents/case-report/${record.id}`, {
        responseType: 'text'
      })

      // สร้าง Blob และ URL
      const blob = new Blob([response.data], { type: 'text/html' })
      const url = URL.createObjectURL(blob)

      // เปิดหน้าต่างใหม่แบบเต็มจอ
      const printWindow = window.open(url, '_blank', 'width=' + screen.width + ',height=' + screen.height)

      if (!printWindow) {
        message.error('ไม่สามารถเปิดหน้าต่างพิมพ์ได้ กรุณาอนุญาตให้เปิด popup')
      } else {
        // ขยายหน้าต่างให้เต็มจอ
        printWindow.moveTo(0, 0)
        printWindow.resizeTo(screen.width, screen.height)

        // ทำความสะอาด URL หลังจาก 1 นาที
        setTimeout(() => URL.revokeObjectURL(url), 60000)
      }
    } catch (error: any) {
      message.error('ไม่สามารถสร้างรายงานคดีได้: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleDelete = async (record: CriminalCase) => {
    try {
      await api.delete(`/criminal-cases/${record.id}`)
      message.success('ลบคดีอาญาสำเร็จ')
      fetchData() // Refresh data
    } catch (err) {
      message.error('ไม่สามารถลบคดีอาญาได้')
    }
  }

  const handleAddNew = () => {
    navigate('/add-criminal-case')
  }

  // Bank Account Handlers
  const handleAddBank = () => {
    setEditingBank(null)
    setBankModalVisible(true)
  }

  const handleEditBank = (record: BankAccount) => {
    setEditingBank(record)
    setBankModalVisible(true)
  }

  const handleDeleteBank = async (bankId: number) => {
    try {
      await api.delete(`/bank-accounts/${bankId}`)
      message.success('ลบบัญชีธนาคารสำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
        fetchData() // Refresh counts
      }
    } catch (err) {
      message.error('ไม่สามารถลบบัญชีธนาคารได้')
    }
  }

  const handleBankModalClose = (success?: boolean) => {
    setBankModalVisible(false)
    setEditingBank(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
      fetchData() // Refresh counts
    }
  }

  // Non-Bank Handlers
  const handleAddNonBank = () => {
    setEditingNonBank(null)
    setNonBankModalVisible(true)
  }

  const handleEditNonBank = (record: NonBankAccount) => {
    setEditingNonBank(record)
    setNonBankModalVisible(true)
  }

  const handleDeleteNonBank = async (id: number) => {
    try {
      await api.delete(`/non-bank-accounts/${id}`)
      message.success('ลบบัญชีผู้ให้บริการสำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
        fetchData() // Refresh counts
      }
    } catch (err) {
      message.error('ไม่สามารถลบบัญชีผู้ให้บริการได้')
    }
  }

  const handleNonBankModalClose = (success?: boolean) => {
    setNonBankModalVisible(false)
    setEditingNonBank(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
      fetchData() // Refresh counts
    }
  }

  // Suspect Handlers
  const handleAddSuspect = () => {
    setEditingSuspect(null)
    setSuspectModalVisible(true)
  }

  const handleEditSuspect = (record: Suspect) => {
    setEditingSuspect(record)
    setSuspectModalVisible(true)
  }

  const handleDeleteSuspect = async (suspectId: number) => {
    try {
      await api.delete(`/suspects/${suspectId}`)
      message.success('ลบผู้ต้องหาสำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
        fetchData() // Refresh counts
      }
    } catch (err) {
      message.error('ไม่สามารถลบผู้ต้องหาได้')
    }
  }

  const handleSuspectModalClose = (success?: boolean) => {
    setSuspectModalVisible(false)
    setEditingSuspect(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
      fetchData() // Refresh counts
    }
  }

  const handlePrintSuspectSummons = async (suspectId: number) => {
    try {
      const response = await api.get(`/documents/suspect-summons/${suspectId}`, {
        responseType: 'blob'
      })

      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')

      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }

      message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียกผู้ต้องหา')
    } catch (err) {
      message.error('ไม่สามารถสร้างหมายเรียกผู้ต้องหาได้')
    }
  }

  const handlePrintSuspectEnvelope = async (suspectId: number) => {
    try {
      const response = await api.get(`/documents/suspect-envelope/${suspectId}`, {
        responseType: 'blob'
      })

      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')

      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }

      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียกผู้ต้องหา')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียกผู้ต้องหาได้')
    }
  }

  // Non-Bank Print Handlers
  const handlePrintNonBankSummons = async (nonBankAccountId: number) => {
    // แสดง Modal เลือกอายัดบัญชีหรือไม่
    Modal.confirm({
      title: 'เลือกประเภทหมายเรียก',
      content: 'คุณต้องการอายัดบัญชีหรือไม่?',
      okText: 'อายัดบัญชี',
      cancelText: 'ไม่อายัดบัญชี',
      onOk: async () => {
        // เลือกอายัดบัญชี
        try {
          const response = await api.get(`/documents/non-bank-summons/${nonBankAccountId}`, {
            params: { freeze_account: true },
            responseType: 'blob'
          })
          const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
          const url = window.URL.createObjectURL(blob)
          const printWindow = window.open(url, '_blank')
          if (printWindow) {
            printWindow.onload = () => {
              setTimeout(() => printWindow.print(), 500)
            }
          }
          message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก (อายัดบัญชี)')
        } catch (err) {
          message.error('ไม่สามารถสร้างหมายเรียก Non-Bank ได้')
          console.error(err)
        }
      },
      onCancel: async () => {
        // เลือกไม่อายัดบัญชี
        try {
          const response = await api.get(`/documents/non-bank-summons/${nonBankAccountId}`, {
            params: { freeze_account: false },
            responseType: 'blob'
          })
          const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
          const url = window.URL.createObjectURL(blob)
          const printWindow = window.open(url, '_blank')
          if (printWindow) {
            printWindow.onload = () => {
              setTimeout(() => printWindow.print(), 500)
            }
          }
          message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก (ไม่อายัดบัญชี)')
        } catch (err) {
          message.error('ไม่สามารถสร้างหมายเรียก Non-Bank ได้')
          console.error(err)
        }
      }
    })
  }

  const handlePrintNonBankEnvelope = async (nonBankAccountId: number) => {
    try {
      const response = await api.get(`/documents/non-bank-envelope/${nonBankAccountId}`, {
        responseType: 'blob'
      })

      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')

      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }

      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียก Non-Bank')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียก Non-Bank ได้')
      console.error(err)
    }
  }

  // ==================== Email Handlers ====================

  const handleOpenEmailModal = async (
    accountType: 'non_bank' | 'payment_gateway' | 'telco_mobile' | 'telco_internet' | 'bank',
    accountId: number
  ) => {
    try {
      // Fetch account details to get provider info and email
      let accountData: any = null
      let providerData: any = null

      if (accountType === 'non_bank') {
        const account = nonBankAccounts.find(a => a.id === accountId)
        if (account) {
          accountData = account
          // Fetch provider email from non_banks table
          try {
            const response = await api.get(`/non-banks/${account.non_bank_id}`)
            providerData = response.data
          } catch (err) {
            console.error('Failed to fetch provider data:', err)
          }
        }
      } else if (accountType === 'payment_gateway') {
        const account = paymentGatewayAccounts.find(a => a.id === accountId)
        if (account) {
          accountData = account
          try {
            const response = await api.get(`/payment-gateways/${account.payment_gateway_id}`)
            providerData = response.data
          } catch (err) {
            console.error('Failed to fetch provider data:', err)
          }
        }
      } else if (accountType === 'telco_mobile') {
        const account = telcoMobileAccounts.find(a => a.id === accountId)
        if (account) {
          accountData = account
          try {
            const response = await api.get(`/telco-mobile/${account.telco_mobile_id}`)
            providerData = response.data
          } catch (err) {
            console.error('Failed to fetch provider data:', err)
          }
        }
      } else if (accountType === 'telco_internet') {
        const account = telcoInternetAccounts.find(a => a.id === accountId)
        if (account) {
          accountData = account
          try {
            const response = await api.get(`/telco-internet/${account.telco_internet_id}`)
            providerData = response.data
          } catch (err) {
            console.error('Failed to fetch provider data:', err)
          }
        }
      }

      if (!accountData) {
        message.error('ไม่พบข้อมูลบัญชี')
        return
      }

      // ตรวจสอบว่าผู้ให้บริการมีอีเมล์หรือไม่
      const providerEmail = providerData?.email || ''
      if (!providerEmail || providerEmail.trim() === '') {
        Modal.warning({
          title: 'ไม่พบข้อมูลอีเมล์',
          content: `ผู้ให้บริการ "${accountData.provider_name || accountData.bank_name}" ยังไม่มีข้อมูลอีเมล์ในระบบ กรุณาเพิ่มอีเมล์ใน Master Data ก่อนส่งหมายเรียก`,
          okText: 'ตกลง'
        })
        return
      }

      // Set modal data
      setEmailAccountType(accountType)
      setEmailAccountId(accountId)
      setEmailProviderName(accountData.provider_name || accountData.bank_name || '')
      setEmailDocumentNumber(accountData.document_number || '')
      setEmailDefaultEmail(providerEmail)
      setEmailAccountNumber(accountData.account_number || '')
      setEmailPhoneNumber(accountData.phone_number || '')
      setEmailIpAddress(accountData.ip_address || '')
      setEmailModalVisible(true)
    } catch (err) {
      message.error('เกิดข้อผิดพลาดในการเปิด Modal')
      console.error(err)
    }
  }

  const handleSendEmail = async (recipientEmail: string, freezeAccount: boolean = false) => {
    try {
      const response = await api.post('/emails/send-summons', {
        account_type: emailAccountType,
        account_id: emailAccountId,
        recipient_email: recipientEmail,
        document_type: 'summons',
        freeze_account: freezeAccount
      })

      if (response.data.status === 'sent') {
        message.success('ส่งหมายเรียกทางอีเมล์สำเร็จ!')
        setEmailModalVisible(false)

        // Refresh case details
        if (selected) {
          fetchCaseDetails(selected.id)
        }
      } else {
        message.error(`ส่งอีเมล์ไม่สำเร็จ: ${response.data.message}`)
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'ไม่สามารถส่งอีเมล์ได้'
      message.error(errorMsg)
      console.error('Email sending error:', err)
      throw err
    }
  }

  // ==================== Payment Gateway Handlers ====================

  const handleAddPaymentGateway = () => {
    setEditingPaymentGateway(null)
    setPaymentGatewayModalVisible(true)
  }

  const handleEditPaymentGateway = (record: PaymentGatewayAccount) => {
    setEditingPaymentGateway(record)
    setPaymentGatewayModalVisible(true)
  }

  const handleDeletePaymentGateway = async (id: number) => {
    try {
      await api.delete(`/payment-gateway-accounts/${id}`)
      message.success('ลบบัญชี Payment Gateway สำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
      }
    } catch (err) {
      message.error('ไม่สามารถลบบัญชี Payment Gateway ได้')
    }
  }

  const handlePaymentGatewayModalClose = (success?: boolean) => {
    setPaymentGatewayModalVisible(false)
    setEditingPaymentGateway(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
    }
  }

  const handlePrintPaymentGatewaySummons = async (paymentGatewayAccountId: number) => {
    try {
      const response = await api.get(`/documents/payment-gateway-summons/${paymentGatewayAccountId}`, {
        responseType: 'blob'
      })
      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')
      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => printWindow.print(), 500)
        }
      }
      message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก Payment Gateway')
    } catch (err) {
      message.error('ไม่สามารถสร้างหมายเรียก Payment Gateway ได้')
      console.error(err)
    }
  }

  const handlePrintPaymentGatewayEnvelope = async (paymentGatewayAccountId: number) => {
    try {
      const response = await api.get(`/documents/payment-gateway-envelope/${paymentGatewayAccountId}`, {
        responseType: 'blob'
      })

      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')

      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }

      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียก Payment Gateway')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียก Payment Gateway ได้')
      console.error(err)
    }
  }

  // ==================== Telco Mobile Handlers ====================

  const handleAddTelcoMobile = () => {
    setEditingTelcoMobile(null)
    setTelcoMobileModalVisible(true)
  }

  const handleEditTelcoMobile = (record: TelcoMobileAccount) => {
    setEditingTelcoMobile(record)
    setTelcoMobileModalVisible(true)
  }

  const handleDeleteTelcoMobile = async (id: number) => {
    try {
      await api.delete(`/telco-mobile-accounts/${id}`)
      message.success('ลบหมายเลขโทรศัพท์สำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
      }
    } catch (err) {
      message.error('ไม่สามารถลบหมายเลขโทรศัพท์ได้')
    }
  }

  const handleTelcoMobileModalClose = (success?: boolean) => {
    setTelcoMobileModalVisible(false)
    setEditingTelcoMobile(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
    }
  }

  const handlePrintTelcoMobileSummons = async (telcoMobileAccountId: number, freezeAccount: boolean = false) => {
    try {
      const response = await api.get(`/documents/telco-mobile-summons/${telcoMobileAccountId}?freeze_account=${freezeAccount}`, {
        responseType: 'blob'
      })
      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')
      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => printWindow.print(), 500)
        }
      }
      message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียกข้อมูลโทรศัพท์')
    } catch (err) {
      message.error('ไม่สามารถสร้างหมายเรียกข้อมูลโทรศัพท์ได้')
      console.error(err)
    }
  }

  const handlePrintTelcoMobileEnvelope = async (telcoMobileAccountId: number) => {
    try {
      const response = await api.get(`/documents/telco-mobile-envelope/${telcoMobileAccountId}`, {
        responseType: 'blob'
      })

      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')

      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }

      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียกข้อมูลโทรศัพท์')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียกข้อมูลโทรศัพท์ได้')
      console.error(err)
    }
  }

  // ==================== Telco Internet (IP Address) Handlers ====================

  const handleAddTelcoInternet = () => {
    setEditingTelcoInternet(null)
    setTelcoInternetModalVisible(true)
  }

  const handleEditTelcoInternet = (record: TelcoInternetAccount) => {
    setEditingTelcoInternet(record)
    setTelcoInternetModalVisible(true)
  }

  const handleDeleteTelcoInternet = async (id: number) => {
    try {
      await api.delete(`/telco-internet-accounts/${id}`)
      message.success('ลบ IP Address สำเร็จ')
      if (selected) {
        fetchCaseDetails(selected.id)
      }
    } catch (err) {
      message.error('ไม่สามารถลบ IP Address ได้')
    }
  }

  const handleTelcoInternetModalClose = (success?: boolean) => {
    setTelcoInternetModalVisible(false)
    setEditingTelcoInternet(null)
    if (success && selected) {
      fetchCaseDetails(selected.id)
    }
  }

  const handlePrintTelcoInternetSummons = async (telcoInternetAccountId: number, freezeAccount: boolean = false) => {
    try {
      const response = await api.get(`/documents/telco-internet-summons/${telcoInternetAccountId}?freeze_account=${freezeAccount}`, {
        responseType: 'blob'
      })
      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')
      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => printWindow.print(), 500)
        }
      }
      message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียกข้อมูล IP Address')
    } catch (err) {
      message.error('ไม่สามารถสร้างหมายเรียกข้อมูล IP Address ได้')
      console.error(err)
    }
  }

  const handlePrintTelcoInternetEnvelope = async (telcoInternetAccountId: number) => {
    try {
      const response = await api.get(`/documents/telco-internet-envelope/${telcoInternetAccountId}`, {
        responseType: 'blob'
      })

      const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const printWindow = window.open(url, '_blank')

      if (printWindow) {
        printWindow.onload = () => {
          setTimeout(() => {
            printWindow.print()
          }, 500)
        }
      }

      message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียกข้อมูล IP Address')
    } catch (err) {
      message.error('ไม่สามารถสร้างซองหมายเรียกข้อมูล IP Address ได้')
      console.error(err)
    }
  }

  const getStatusTextStyle = (status: string, complaintDate?: string) => {
    if (status === 'จำหน่าย') {
      return { color: 'green' }
    }
    
    if (status === 'อยู่ระหว่างสอบสวน' && complaintDate) {
      const complaintDateObj = new Date(complaintDate)
      const now = new Date()
      const diffTime = now.getTime() - complaintDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays > 180) { // 6 months = ~180 days
        return { color: 'red' }
      }
    }
    
    return {}
  }

  const getRowClassName = (record: CriminalCase) => {
    // ถ้าสถานะคดีเป็น 'จำหน่าย' ให้ใช้สีพื้นหลังเขียวอ่อน
    if (record.status === 'จำหน่าย') {
      return 'row-closed-case'
    }
    
    // ถ้าสถานะคดีเป็น 'ระหว่างสอบสวน' และเกิน 6 เดือน ให้ใช้สีแดงอ่อน
    if (record.status === 'ระหว่างสอบสวน' && record.complaint_date) {
      const complaintDateObj = new Date(record.complaint_date)
      const now = new Date()
      const diffTime = now.getTime() - complaintDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      
      if (diffDays > 180) { // 6 months = ~180 days
        return 'row-red'
      }
    }
    
    return ''
  }

  const calculateCaseAge = (complaintDate?: string) => {
    if (!complaintDate) return '-'
    
    try {
      const complaintDateObj = new Date(complaintDate)
      const now = new Date()
      const diffTime = now.getTime() - complaintDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      const months = Math.floor(diffDays / 30)
      const remainingDays = diffDays % 30
      
      if (months > 0) {
        return `${months} เดือน ${remainingDays} วัน`
      } else {
        return `${remainingDays} วัน`
      }
    } catch {
      return '-'
    }
  }

  const calculateDaysSinceSent = (documentDate?: string) => {
    if (!documentDate) return '-'
    
    try {
      const documentDateObj = new Date(documentDate)
      const now = new Date()
      const diffTime = now.getTime() - documentDateObj.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      const months = Math.floor(diffDays / 30)
      const remainingDays = diffDays % 30
      
      if (months > 0) {
        return `${months} เดือน ${remainingDays} วัน`
      } else {
        return `${remainingDays} วัน`
      }
    } catch {
      return '-'
    }
  }


  const columns: ColumnsType<CriminalCase> = [
    {
      title: 'ลำดับ',
      key: 'row_number',
      width: 80,
      render: (_, __, index) => index + 1,
      filters: [
        { text: '1-10', value: '1-10' },
        { text: '11-20', value: '11-20' },
        { text: '21-30', value: '21-30' },
        { text: '31+', value: '31+' },
      ],
      onFilter: (value: any, record: CriminalCase) => {
        // สำหรับคอลัมน์ลำดับ เราจะใช้ index จาก dataSource
        const index = data.findIndex(item => item.id === record.id)
        const num = index + 1
        switch (value) {
          case '1-10': return num >= 1 && num <= 10
          case '11-20': return num >= 11 && num <= 20
          case '21-30': return num >= 21 && num <= 30
          case '31+': return num >= 31
          default: return true
        }
      },
    },
    {
      title: 'สถานะคดี',
      dataIndex: 'status',
      key: 'status',
      render: (status: string, record: CriminalCase) => {
        const textStyle = getStatusTextStyle(status, record.complaint_date)
        return <Tag color="blue" style={textStyle}>{status}</Tag>
      },
      filters: [
        { text: 'ระหว่างสอบสวน', value: 'ระหว่างสอบสวน' },
        { text: 'จำหน่าย', value: 'จำหน่าย' },
      ],
      onFilter: (value: any, record: CriminalCase) => record.status === value,
    },
    {
      title: 'เลขที่คดี',
      dataIndex: 'case_number',
      key: 'case_number',
      render: (_, record: CriminalCase) => (
        <Button type="link" onClick={() => showDetails(record)}>
          {record.case_number}
        </Button>
      ),
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
        <div style={{ padding: 8 }}>
          <Input
            placeholder="ค้นหาเลขที่คดี"
            value={selectedKeys[0]}
            onChange={(e: any) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
            onPressEnter={() => confirm()}
            style={{ width: 188, marginBottom: 8, display: 'block' }}
          />
          <Space>
            <Button
              type="primary"
              onClick={() => confirm()}
              size="small"
              style={{ width: 90 }}
            >
              ค้นหา
            </Button>
            <Button onClick={() => clearFilters && clearFilters()} size="small" style={{ width: 90 }}>
              รีเซ็ต
            </Button>
          </Space>
        </div>
      ),
      onFilter: (value: any, record: CriminalCase) =>
        record.case_number?.toLowerCase().includes((value as string).toLowerCase()) || false,
    },
    {
      title: 'CaseID',
      dataIndex: 'case_id',
      key: 'case_id',
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
        <div style={{ padding: 8 }}>
          <Input
            placeholder="ค้นหา CaseID"
            value={selectedKeys[0]}
            onChange={(e: any) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
            onPressEnter={() => confirm()}
            style={{ width: 188, marginBottom: 8, display: 'block' }}
          />
          <Space>
            <Button
              type="primary"
              onClick={() => confirm()}
              size="small"
              style={{ width: 90 }}
            >
              ค้นหา
            </Button>
            <Button onClick={() => clearFilters && clearFilters()} size="small" style={{ width: 90 }}>
              รีเซ็ต
            </Button>
          </Space>
        </div>
      ),
      onFilter: (value: any, record: CriminalCase) =>
        record.case_id?.toLowerCase().includes((value as string).toLowerCase()) || false,
    },
    {
      title: 'ผู้ร้องทุกข์',
      dataIndex: 'complainant',
      key: 'complainant',
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
        <div style={{ padding: 8 }}>
          <Input
            placeholder="ค้นหาผู้ร้องทุกข์"
            value={selectedKeys[0]}
            onChange={(e: any) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
            onPressEnter={() => confirm()}
            style={{ width: 188, marginBottom: 8, display: 'block' }}
          />
          <Space>
            <Button
              type="primary"
              onClick={() => confirm()}
              size="small"
              style={{ width: 90 }}
            >
              ค้นหา
            </Button>
            <Button onClick={() => clearFilters && clearFilters()} size="small" style={{ width: 90 }}>
              รีเซ็ต
            </Button>
          </Space>
        </div>
      ),
      onFilter: (value: any, record: CriminalCase) =>
        record.complainant?.toLowerCase().includes((value as string).toLowerCase()) || false,
    },
    {
      title: 'วันที่/เวลา รับคำร้องทุกข์',
      dataIndex: 'complaint_date',
      key: 'complaint_date',
      render: (date: string) => formatThaiDate(date),
      sorter: (a, b) => {
        if (!a.complaint_date && !b.complaint_date) return 0
        if (!a.complaint_date) return 1
        if (!b.complaint_date) return -1
        return new Date(a.complaint_date).getTime() - new Date(b.complaint_date).getTime()
      },
      defaultSortOrder: 'descend',
    },
    {
      title: 'เขตอำนาจศาล',
      dataIndex: 'court_name',
      key: 'court_name',
      render: (courtName: string) => courtName || '-',
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
        <div style={{ padding: 8 }}>
          <Input
            placeholder="ค้นหาเขตอำนาจศาล"
            value={selectedKeys[0]}
            onChange={(e: any) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
            onPressEnter={() => confirm()}
            style={{ width: 188, marginBottom: 8, display: 'block' }}
          />
          <Space>
            <Button
              type="primary"
              onClick={() => confirm()}
              size="small"
              style={{ width: 90 }}
            >
              ค้นหา
            </Button>
            <Button onClick={() => clearFilters && clearFilters()} size="small" style={{ width: 90 }}>
              รีเซ็ต
            </Button>
          </Space>
        </div>
      ),
      onFilter: (value: any, record: CriminalCase) =>
        (record.court_name || '').toLowerCase().includes((value as string).toLowerCase()),
    },
    {
      title: 'อายุคดี',
      dataIndex: 'complaint_date',
      key: 'case_age',
      render: (date: string) => calculateCaseAge(date),
      filters: [
        { text: '0-30 วัน', value: '0-30' },
        { text: '31-90 วัน', value: '31-90' },
        { text: '91-180 วัน', value: '91-180' },
        { text: '181-365 วัน', value: '181-365' },
        { text: 'มากกว่า 1 ปี', value: '365+' },
      ],
      onFilter: (value: any, record: CriminalCase) => {
        if (!record.complaint_date) return false
        const complaintDate = new Date(record.complaint_date)
        const now = new Date()
        const diffTime = Math.abs(now.getTime() - complaintDate.getTime())
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        
        switch (value) {
          case '0-30': return diffDays <= 30
          case '31-90': return diffDays >= 31 && diffDays <= 90
          case '91-180': return diffDays >= 91 && diffDays <= 180
          case '181-365': return diffDays >= 181 && diffDays <= 365
          case '365+': return diffDays > 365
          default: return true
        }
      },
    },
    {
      title: 'จำนวนบัญชีธนาคาร',
      dataIndex: 'bank_accounts_count',
      key: 'bank_accounts_count',
      filters: [
        { text: '0 บัญชี', value: '0' },
        { text: '1-5 บัญชี', value: '1-5' },
        { text: '6-10 บัญชี', value: '6-10' },
        { text: 'มากกว่า 10 บัญชี', value: '10+' },
      ],
      onFilter: (value: any, record: CriminalCase) => {
        const count = parseInt(record.bank_accounts_count || '0')
        switch (value) {
          case '0': return count === 0
          case '1-5': return count >= 1 && count <= 5
          case '6-10': return count >= 6 && count <= 10
          case '10+': return count > 10
          default: return true
        }
      },
    },
    {
      title: 'จำนวน ผู้ต้องหาที่เกี่ยวข้อง',
      dataIndex: 'suspects_count',
      key: 'suspects_count',
      filters: [
        { text: '0 คน', value: '0' },
        { text: '1-3 คน', value: '1-3' },
        { text: '4-6 คน', value: '4-6' },
        { text: 'มากกว่า 6 คน', value: '6+' },
      ],
      onFilter: (value: any, record: CriminalCase) => {
        const count = parseInt(record.suspects_count || '0')
        switch (value) {
          case '0': return count === 0
          case '1-3': return count >= 1 && count <= 3
          case '4-6': return count >= 4 && count <= 6
          case '6+': return count > 6
          default: return true
        }
      },
    },
    {
      title: 'จัดการ',
      key: 'actions',
      render: (_, record: CriminalCase) => (
        <Space>
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
            title="แก้ไขคดี"
          />
          <Button
            type="text"
            icon={<PrinterOutlined />}
            onClick={() => handlePrintCaseReport(record)}
            title="พิมพ์รายงานคดี"
          />
          <Popconfirm
            title="คุณแน่ใจหรือไม่ที่จะลบคดีนี้?"
            onConfirm={() => handleDelete(record)}
            okText="ใช่"
            cancelText="ไม่"
          >
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
              title="ลบคดี"
            />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  if (!token || !user) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>กำลังตรวจสอบการเข้าสู่ระบบ...</p>
      </div>
    )
  }

  return (
    <div style={{ padding: '20px' }}>
      {/* หัวข้อและแถบสถิติ */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ margin: 0 }}>คดีอาญาในความรับผิดชอบ</h1>
            {user && (
              <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
                <span style={{ fontWeight: '500' }}>
                  {user.rank?.rank_short} {user.full_name}
                </span>
                {user.position && (
                  <span style={{ marginLeft: '8px', color: '#999' }}>
                    ({user.position})
                  </span>
                )}
              </div>
            )}
          </div>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAddNew}>
            เพิ่มคดีใหม่
          </Button>
        </div>
        
        {/* แถบสถิติ */}
        <div style={{ 
          padding: '12px 16px', 
          backgroundColor: '#f0f8ff', 
          border: '1px solid #d9d9d9', 
          borderRadius: '6px',
          fontSize: '14px',
          fontWeight: '500',
          color: '#1890ff'
        }}>
          <span style={{ marginRight: '20px' }}>
            จำนวนคดีทั้งหมด: <strong>{stats.totalCases}</strong>
          </span>
          <span style={{ marginRight: '20px' }}>
            กำลังดำเนินการ: <strong style={{ color: '#52c41a' }}>{stats.processingCases}</strong>
          </span>
          <span style={{ marginRight: '20px' }}>
            เกิน 6 เดือน: <strong style={{ color: '#fa8c16' }}>{stats.over6MonthsCases}</strong>
          </span>
          <span>
            จำหน่ายแล้ว: <strong style={{ color: '#722ed1' }}>{stats.closedCases}</strong>
          </span>
        </div>
      </div>

      <Table
        columns={columns}
        dataSource={data}
        loading={loading}
        rowKey="id"
        rowClassName={getRowClassName}
        pagination={{
          pageSize: 20,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => `${range[0]}-${range[1]} จาก ${total} รายการ`,
        }}
      />

      <Drawer
        title={
          `รายละเอียดคดี ${selected?.case_number || ''}${selected?.case_id ? ` | CaseID: ${selected.case_id}` : ''} ${
            selected?.complainant
              ? `(${selected.complainant.replace(/^\d+\)\s*/, '')})`
              : ''
          }`
        }
        placement="right"
        width="70%"
        onClose={() => setOpen(false)}
        open={open}
      >
        {selected && (
          <Tabs defaultActiveKey="general">
            <Tabs.TabPane tab="📋 ข้อมูลทั่วไป" key="general">
              <Descriptions column={2} bordered>
                <Descriptions.Item label="เลขที่คดี">{selected.case_number || '-'}</Descriptions.Item>
                <Descriptions.Item label="CaseID">{selected.case_id || '-'}</Descriptions.Item>
                <Descriptions.Item label="สถานะคดี">{selected.status}</Descriptions.Item>
                <Descriptions.Item label="ประเภทคดี">{selected.case_type || '-'}</Descriptions.Item>
                <Descriptions.Item label="ผู้ร้องทุกข์">{selected.complainant}</Descriptions.Item>
                <Descriptions.Item label="วันที่/เวลา รับคำร้องทุกข์">
                  {selected.complaint_date_thai || '-'}
                </Descriptions.Item>
                <Descriptions.Item label="อายุคดี">
                  {calculateCaseAge(selected.complaint_date)}
                </Descriptions.Item>
                <Descriptions.Item label="ความเสียหาย">
                  {selected.damage_amount || '-'}
                </Descriptions.Item>
                <Descriptions.Item label="สถานที่เกิดเหตุ">
                  -
                </Descriptions.Item>
              </Descriptions>
            </Tabs.TabPane>

            <Tabs.TabPane tab={<span><FileExcelOutlined /> ข้อมูล CFR ({cfrFiles.length})</span>} key="cfr">
              <Card>
                <Space direction="vertical" style={{ width: '100%' }} size="large">
                  <div>
                    <h3>อัพโหลดไฟล์ CFR (Central Fraud Registry)</h3>
                    <p style={{ color: '#666' }}>
                      อัพโหลดไฟล์ข้อมูลเส้นทางการเงิน (.xlsx) จาก CFR System
                      <br />
                      หากชื่อไฟล์ซ้ำกับที่มีอยู่แล้ว ระบบจะลบข้อมูลเดิมและนำเข้าข้อมูลใหม่แทน
                    </p>
                  </div>
                  <Upload
                    accept=".xlsx"
                    beforeUpload={handleCfrUpload}
                    showUploadList={false}
                    disabled={uploadingCfr}
                  >
                    <Button 
                      type="primary" 
                      icon={<UploadOutlined />}
                      loading={uploadingCfr}
                    >
                      {uploadingCfr ? 'กำลังอัพโหลด...' : 'อัพโหลดไฟล์ CFR'}
                    </Button>
                  </Upload>

                  <div>
                    <h4>ไฟล์ที่อัพโหลดแล้ว</h4>
                    {cfrFiles.length === 0 ? (
                      <p style={{ color: '#999' }}>ยังไม่มีไฟล์ CFR</p>
                    ) : (
                      <List
                        bordered
                        dataSource={cfrFiles}
                        renderItem={(item: any) => (
                          <List.Item
                            actions={[
                              <Popconfirm
                                title="คุณแน่ใจหรือไม่ที่จะลบไฟล์นี้?"
                                description={`จะลบข้อมูล ${item.record_count} รายการ`}
                                onConfirm={() => handleDeleteCfrFile(item.filename)}
                                okText="ใช่"
                                cancelText="ไม่"
                              >
                                <Button type="link" danger icon={<DeleteOutlined />}>
                                  ลบ
                                </Button>
                              </Popconfirm>
                            ]}
                          >
                            <List.Item.Meta
                              avatar={<FileExcelOutlined style={{ fontSize: 24, color: '#52c41a' }} />}
                              title={item.filename}
                              description={
                                <Space direction="vertical" size={0}>
                                  <span>จำนวนรายการ: {item.record_count} รายการ</span>
                                  <span>อัพโหลดล่าสุด: {new Date(item.last_upload).toLocaleString('th-TH')}</span>
                                </Space>
                              }
                            />
                          </List.Item>
                        )}
                      />
                    )}
                  </div>

                  {/* แสดงข้อมูล CFR แยกตาราง 1 ตารางต่อ 1 bank_case_id */}
                  <div style={{ marginTop: 32 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                      <h3 style={{ margin: 0 }}>ข้อมูลเส้นทางการเงิน</h3>
                      {cfrRecords.length > 0 && (
                        <Button 
                          type="primary"
                          icon={<ApartmentOutlined />}
                          onClick={() => setFlowChartVisible(true)}
                        >
                          แสดงแผนผังเส้นทางการเงิน
                        </Button>
                      )}
                    </div>
                    {loadingCfr ? (
                      <Spin />
                    ) : cfrRecords.length === 0 ? (
                      <p style={{ color: '#999' }}>ยังไม่มีข้อมูล CFR</p>
                    ) : (
                      <>
                        {/* แยกข้อมูลตาม bank_case_id */}
                        {Array.from(new Set(cfrRecords.map(r => r.bank_case_id))).map((bankCaseId) => {
                          const records = cfrRecords
                            .filter(r => r.bank_case_id === bankCaseId)
                            .sort((a, b) => {
                              // เรียงตาม transfer_date ก่อน
                              const dateCompare = (a.transfer_date || '').localeCompare(b.transfer_date || '')
                              if (dateCompare !== 0) return dateCompare
                              // ถ้าวันเดียวกัน เรียงตาม transfer_time
                              return (a.transfer_time || '').localeCompare(b.transfer_time || '')
                            })
                          return (
                            <Card 
                              key={bankCaseId} 
                              style={{ marginBottom: 16 }}
                              title={`Bank Case ID: ${bankCaseId} (${records.length} รายการ)`}
                              size="small"
                            >
                              <Table
                                dataSource={records}
                                rowKey="id"
                                size="small"
                                pagination={{ pageSize: 10 }}
                                scroll={{ x: 900 }}
                                columns={[
                                  {
                                    title: 'บัญชีต้นทาง',
                                    key: 'from_account',
                                    width: 250,
                                    render: (_, record) => {
                                      const isVictim = isVictimAccount(record.from_account_name)
                                      const summons = findBankAccountSummons(record.from_account_no)
                                      const shortName = record.from_bank_short_name
                                      const logoUrl = shortName ? `/Bank-icons/${shortName}.png` : ''
                                      
                                      return (
                                        <div
                                          style={{
                                            position: 'relative',
                                            padding: '12px 16px',
                                            minHeight: '60px',
                                            overflow: 'hidden',
                                          }}
                                        >
                                          {logoUrl && (
                                            <div
                                              style={{
                                                position: 'absolute',
                                                top: '50%',
                                                left: '50%',
                                                transform: 'translate(-50%, -50%)',
                                                width: '100%',
                                                height: '100%',
                                                backgroundImage: `url(${logoUrl})`,
                                                backgroundSize: 'cover',
                                                backgroundRepeat: 'no-repeat',
                                                backgroundPosition: 'center',
                                                opacity: 0.05,
                                                zIndex: 0,
                                              }}
                                            />
                                          )}
                                          <div style={{ position: 'relative', zIndex: 1 }}>
                                            <div>
                                              <strong>{record.from_bank_short_name || '-'}</strong>
                                              {isVictim && (
                                                <Tag color="green" style={{ marginLeft: 4, fontSize: '10px' }}>
                                                  ผู้เสียหาย
                                                </Tag>
                                              )}
                                              {summons && (
                                                <Tag color="purple" style={{ marginLeft: 4, fontSize: '10px' }}>
                                                  ส่งหมายเรียกแล้ว
                                                </Tag>
                                              )}
                                            </div>
                                            <div>{record.from_account_no || '-'}</div>
                                            <div style={{ color: '#666', fontSize: '11px' }}>
                                              {record.from_account_name || '-'}
                                            </div>
                                            {summons && (
                                              <div style={{ fontSize: '10px', color: '#722ed1', marginTop: 2 }}>
                                                {summons.reply_status ? '✓ ได้รับข้อมูลแล้ว' : `✗ ยังไม่ตอบกลับ (ส่งไปแล้ว ${calculateDaysSinceSent(summons.document_date)})`}
                                              </div>
                                            )}
                                          </div>
                                        </div>
                                      )
                                    },
                                  },
                                  {
                                    title: 'บัญชีปลายทาง',
                                    key: 'to_account',
                                    width: 250,
                                    render: (_, record) => {
                                      const isVictim = isVictimAccount(record.to_account_name)
                                      const summons = findBankAccountSummons(record.to_account_no)
                                      const shortName = record.to_bank_short_name
                                      const logoUrl = shortName ? `/Bank-icons/${shortName}.png` : ''
                                      
                                      return (
                                        <div
                                          style={{
                                            position: 'relative',
                                            padding: '12px 16px',
                                            minHeight: '60px',
                                            overflow: 'hidden',
                                            width: '100%',
                                            cursor: 'pointer',
                                          }}
                                          onClick={() => showCfrAccountDetail(record)}
                                        >
                                          {logoUrl && (
                                            <div
                                              style={{
                                                position: 'absolute',
                                                top: '50%',
                                                left: '50%',
                                                transform: 'translate(-50%, -50%)',
                                                width: '100%',
                                                height: '100%',
                                                backgroundImage: `url(${logoUrl})`,
                                                backgroundSize: 'cover',
                                                backgroundRepeat: 'no-repeat',
                                                backgroundPosition: 'center',
                                                opacity: 0.05,
                                                zIndex: 0,
                                              }}
                                            />
                                          )}
                                          <div style={{ position: 'relative', zIndex: 1 }}>
                                            <div>
                                              <strong style={{ color: '#1890ff' }}>{record.to_bank_short_name || '-'}</strong>
                                              {isVictim && (
                                                <Tag color="green" style={{ marginLeft: 4, fontSize: '10px' }}>
                                                  ผู้เสียหาย
                                                </Tag>
                                              )}
                                              {summons && (
                                                <Tag color="purple" style={{ marginLeft: 4, fontSize: '10px' }}>
                                                  ส่งหมายเรียกแล้ว
                                                </Tag>
                                              )}
                                            </div>
                                            <div style={{ color: '#1890ff', textDecoration: 'underline' }}>{record.to_account_no || '-'}</div>
                                            <div style={{ color: '#666', fontSize: '11px' }}>
                                              {record.to_account_name || '-'}
                                            </div>
                                            {summons && (
                                              <div style={{ fontSize: '10px', color: '#722ed1', marginTop: 2 }}>
                                                {summons.reply_status ? '✓ ได้รับข้อมูลแล้ว' : `✗ ยังไม่ตอบกลับ (ส่งไปแล้ว ${calculateDaysSinceSent(summons.document_date)})`}
                                              </div>
                                            )}
                                            {!summons && !isVictim && (
                                              <Button 
                                                type="primary" 
                                                size="small" 
                                                style={{ marginTop: 4, fontSize: '10px', height: '20px' }}
                                                onClick={(e) => {
                                                  e.stopPropagation()
                                                  handleCreateSummonsFromCfr(record)
                                                }}
                                              >
                                                สร้างหมายเรียก
                                              </Button>
                                            )}
                                          </div>
                                        </div>
                                      )
                                    },
                                  },
                                  {
                                    title: 'วันเวลาที่โอน',
                                    key: 'transfer_datetime',
                                    width: 150,
                                    render: (_, record) => (
                                      <div>
                                        <div>{record.transfer_date || '-'}</div>
                                        <div style={{ color: '#666', fontSize: '11px' }}>
                                          {record.transfer_time || '-'}
                                        </div>
                                      </div>
                                    ),
                                  },
                                  {
                                    title: 'ยอดเงินที่โอน',
                                    dataIndex: 'transfer_amount',
                                    key: 'transfer_amount',
                                    width: 150,
                                    align: 'right',
                                    render: (amount) => amount ? Number(amount).toLocaleString('th-TH', {
                                      minimumFractionDigits: 2,
                                      maximumFractionDigits: 2
                                    }) + ' ฿' : '-',
                                  },
                                  {
                                    title: 'หมายเหตุ',
                                    key: 'note',
                                    width: 180,
                                    render: (_, record) => {
                                      const sequence = getVictimTransferSequence(record, records)
                                      if (sequence) {
                                        return (
                                          <Tag color="orange" style={{ fontSize: '11px', fontWeight: 'bold' }}>
                                            ผู้เสียหายโอนครั้งที่ {sequence}
                                          </Tag>
                                        )
                                      }
                                      return '-'
                                    },
                                  },
                                ]}
                              />
                            </Card>
                          )
                        })}
                      </>
                    )}
                  </div>
                </Space>
              </Card>
            </Tabs.TabPane>

            <Tabs.TabPane tab={`🏦 บัญชีธนาคารที่เกี่ยวข้อง (${bankAccounts.length})`} key="bank-accounts">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddBank}
                >
                  เพิ่มบัญชีธนาคาร
                </Button>
              </Space>
              <Table
                dataSource={bankAccounts}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date',
                    key: 'document_date',
                    render: (date) => formatThaiDate(date),
                  },
                  {
                    title: 'ชื่อธนาคาร',
                    dataIndex: 'bank_name',
                    key: 'bank_name',
                    width: 250,
                    render: (bankName: string) => {
                      const shortName = getBankShortName(bankName)
                      const logoUrl = shortName ? `/Bank-icons/${shortName}.png` : ''
                      
                      return (
                        <div
                          style={{
                            position: 'relative',
                            padding: '12px 16px',
                            minHeight: '60px',
                            display: 'flex',
                            alignItems: 'center',
                            overflow: 'hidden',
                          }}
                        >
                          {logoUrl && (
                            <div
                              style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                width: '100%',
                                height: '100%',
                                backgroundImage: `url(${logoUrl})`,
                                backgroundSize: 'cover',
                                backgroundRepeat: 'no-repeat',
                                backgroundPosition: 'center',
                                opacity: 0.05,
                                zIndex: 0,
                              }}
                            />
                          )}
                          <span
                            style={{
                              position: 'relative',
                              zIndex: 1,
                              fontWeight: 600,
                              fontSize: '14px',
                              color: '#000',
                              textShadow: '0 0 4px white, 0 0 4px white, 0 0 4px white',
                              width: '100%',
                            }}
                          >
                            {bankName || '-'}
                          </span>
                        </div>
                      )
                    },
                  },
                  {
                    title: 'เลขบัญชี',
                    dataIndex: 'account_number',
                    key: 'account_number',
                  },
                  {
                    title: 'ชื่อบัญชี',
                    dataIndex: 'account_name',
                    key: 'account_name',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: BankAccount) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การดำเนินการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            size="small"
                            icon={<EditOutlined />}
                            onClick={() => handleEditBank(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="คุณแน่ใจหรือไม่ที่จะลบบัญชีนี้?"
                            onConfirm={() => handleDeleteBank(record.id)}
                            okText="ใช่"
                            cancelText="ไม่"
                          >
                            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => {
                            // แสดง Modal เลือกอายัดบัญชีหรือไม่
                            Modal.confirm({
                              title: 'เลือกประเภทหมายเรียก',
                              content: 'คุณต้องการอายัดบัญชีหรือไม่?',
                              okText: 'อายัดบัญชี',
                              cancelText: 'ไม่อายัดบัญชี',
                              onOk: async () => {
                                // เลือกอายัดบัญชี
                                try {
                                  const response = await api.get(`/documents/bank-summons/${record.id}`, {
                                    params: { freeze_account: true },
                                    responseType: 'blob'
                                  })
                                  const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
                                  const url = window.URL.createObjectURL(blob)
                                  const printWindow = window.open(url, '_blank')
                                  if (printWindow) {
                                    printWindow.onload = () => {
                                      setTimeout(() => printWindow.print(), 500)
                                    }
                                  }
                                  message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก (อายัดบัญชี)')
                                } catch (err) {
                                  message.error('ไม่สามารถสร้างหมายเรียกได้')
                                }
                              },
                              onCancel: async () => {
                                // เลือกไม่อายัดบัญชี
                                try {
                                  const response = await api.get(`/documents/bank-summons/${record.id}`, {
                                    params: { freeze_account: false },
                                    responseType: 'blob'
                                  })
                                  const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
                                  const url = window.URL.createObjectURL(blob)
                                  const printWindow = window.open(url, '_blank')
                                  if (printWindow) {
                                    printWindow.onload = () => {
                                      setTimeout(() => printWindow.print(), 500)
                                    }
                                  }
                                  message.success('กำลังเปิดหน้าต่างพิมพ์หมายเรียก (ไม่อายัดบัญชี)')
                                } catch (err) {
                                  message.error('ไม่สามารถสร้างหมายเรียกได้')
                                }
                              }
                            })
                          }}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={async () => {
                            try {
                              const response = await api.get(`/documents/bank-envelope/${record.id}`, {
                                responseType: 'blob'
                              })
                              const blob = new Blob([response.data], { type: 'text/html; charset=utf-8' })
                              const url = window.URL.createObjectURL(blob)
                              const printWindow = window.open(url, '_blank')
                              if (printWindow) {
                                printWindow.onload = () => {
                                  setTimeout(() => printWindow.print(), 500)
                                }
                              }
                              message.success('กำลังเปิดหน้าต่างพิมพ์ซองหมายเรียก')
                            } catch (err) {
                              message.error('ไม่สามารถสร้างซองหมายเรียกได้')
                            }
                          }}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>

            <Tabs.TabPane tab={`🏪 Non-Bank (${nonBankAccounts.length})`} key="non-bank-accounts">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddNonBank}
                >
                  เพิ่มบัญชีผู้ให้บริการ
                </Button>
              </Space>
              <Table
                dataSource={nonBankAccounts}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date',
                    key: 'document_date',
                    render: (date) => formatThaiDate(date),
                  },
                  {
                    title: 'ชื่อผู้ให้บริการ',
                    dataIndex: 'provider_name',
                    key: 'provider_name',
                    width: 250,
                    render: (providerName: string) => {
                      const shortName = getNonBankShortName(providerName)
                      const logoUrl = shortName ? `/Bank-icons/${shortName}.png` : ''
                      
                      return (
                        <div
                          style={{
                            position: 'relative',
                            padding: '12px 16px',
                            minHeight: '60px',
                            display: 'flex',
                            alignItems: 'center',
                            overflow: 'hidden',
                          }}
                        >
                          {logoUrl && (
                            <div
                              style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                width: '100%',
                                height: '100%',
                                backgroundImage: `url(${logoUrl})`,
                                backgroundSize: 'cover',
                                backgroundRepeat: 'no-repeat',
                                backgroundPosition: 'center',
                                opacity: 0.05,
                                zIndex: 0,
                              }}
                            />
                          )}
                          <span
                            style={{
                              position: 'relative',
                              zIndex: 1,
                              fontWeight: 600,
                              fontSize: '14px',
                              color: '#000',
                              textShadow: '0 0 4px white, 0 0 4px white, 0 0 4px white',
                              width: '100%',
                            }}
                          >
                            {providerName || '-'}
                          </span>
                        </div>
                      )
                    },
                  },
                  {
                    title: 'เลขบัญชี',
                    dataIndex: 'account_number',
                    key: 'account_number',
                  },
                  {
                    title: 'ชื่อบัญชี',
                    dataIndex: 'account_name',
                    key: 'account_name',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: NonBankAccount) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การจัดการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            size="small"
                            icon={<EditOutlined />}
                            onClick={() => handleEditNonBank(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="ยืนยันการลบบัญชีผู้ให้บริการ?"
                            onConfirm={() => handleDeleteNonBank(record.id)}
                            okText="ยืนยัน"
                            cancelText="ยกเลิก"
                          >
                            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintNonBankSummons(record.id)}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintNonBankEnvelope(record.id)}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                        <Button
                          type="default"
                          size="small"
                          icon={<MailOutlined />}
                          onClick={() => handleOpenEmailModal('non_bank', record.id)}
                          block
                          style={{ borderColor: '#1890ff', color: '#1890ff' }}
                        >
                          ส่งอีเมล์
                        </Button>
                        <Button
                          size="small"
                          icon={<HistoryOutlined />}
                          onClick={() => handleShowEmailHistory('non_bank', record.id, {
                            documentNumber: record.document_number,
                            providerName: record.provider_name,
                            accountNumber: record.account_number
                          })}
                          block
                          style={{ borderColor: '#722ed1', color: '#722ed1' }}
                        >
                          ประวัติอีเมล์
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>

            <Tabs.TabPane tab={`💳 Payment Gateway (${paymentGatewayAccounts.length})`} key="payment-gateway-accounts">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddPaymentGateway}
                >
                  เพิ่มบัญชี Payment Gateway
                </Button>
              </Space>
              <Table
                dataSource={paymentGatewayAccounts}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date',
                    key: 'document_date',
                    render: (date) => formatThaiDate(date),
                  },
                  {
                    title: 'Payment Gateway',
                    dataIndex: 'provider_name',
                    key: 'provider_name',
                    width: 200,
                    render: (providerName: string) => {
                      const shortName = getNonBankShortName(providerName)
                      const logoUrl = shortName ? `/Bank-icons/${shortName}.png` : ''
                      
                      return (
                        <div
                          style={{
                            position: 'relative',
                            padding: '12px 16px',
                            minHeight: '60px',
                            display: 'flex',
                            alignItems: 'center',
                            overflow: 'hidden',
                          }}
                        >
                          {logoUrl && (
                            <div
                              style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                width: '100%',
                                height: '100%',
                                backgroundImage: `url(${logoUrl})`,
                                backgroundSize: 'cover',
                                backgroundRepeat: 'no-repeat',
                                backgroundPosition: 'center',
                                opacity: 0.05,
                                zIndex: 0,
                              }}
                            />
                          )}
                          <span
                            style={{
                              position: 'relative',
                              zIndex: 1,
                              fontWeight: 600,
                              fontSize: '14px',
                              color: '#000',
                              textShadow: '0 0 4px white, 0 0 4px white, 0 0 4px white',
                              width: '100%',
                            }}
                          >
                            {providerName || '-'}
                          </span>
                        </div>
                      )
                    },
                  },
                  {
                    title: 'ธนาคาร',
                    dataIndex: 'bank_name',
                    key: 'bank_name',
                    width: 200,
                    render: (bankName: string) => {
                      // หา bank_short_name จาก bank_name
                      const getBankShortName = (name: string): string => {
                        if (!name) return ''
                        const bankMap: { [key: string]: string } = {
                          'กรุงเทพ': 'BBL',
                          'BBL': 'BBL',
                          'กสิกรไทย': 'KBANK',
                          'KBANK': 'KBANK',
                          'กรุงไทย': 'KTB',
                          'KTB': 'KTB',
                          'ทหารไทย': 'TMB',
                          'TMB': 'TMB',
                          'ไทยพาณิชย์': 'SCB',
                          'SCB': 'SCB',
                          'กรุงศรีอยุธยา': 'BAY',
                          'BAY': 'BAY',
                          'ธนชาต': 'TBANK',
                          'TBANK': 'TBANK',
                          'ทิสโก้': 'TISCO',
                          'TISCO': 'TISCO',
                          'เกียรตินาคิน': 'KKP',
                          'KKP': 'KKP',
                          'ซีไอเอ็มบี': 'CIMB',
                          'CIMB': 'CIMB',
                          'ยูโอบี': 'UOB',
                          'UOB': 'UOB',
                          'ธ.ก.ส.': 'BAAC',
                          'BAAC': 'BAAC',
                          'ออมสิน': 'GSB',
                          'GSB': 'GSB',
                          'อาคารสงเคราะห์': 'GHB',
                          'GHB': 'GHB',
                          'อิสลาม': 'ISBT',
                          'ISBT': 'ISBT',
                        }
                        
                        for (const [fullName, shortName] of Object.entries(bankMap)) {
                          if (name.includes(fullName) || fullName.includes(name)) {
                            return shortName
                          }
                        }
                        return ''
                      }
                      
                      const shortName = getBankShortName(bankName)
                      const logoUrl = shortName ? `/Bank-icons/${shortName}.png` : ''
                      
                      return (
                        <div
                          style={{
                            position: 'relative',
                            padding: '12px 16px',
                            minHeight: '60px',
                            display: 'flex',
                            alignItems: 'center',
                            overflow: 'hidden',
                          }}
                        >
                          {logoUrl && (
                            <div
                              style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                width: '100%',
                                height: '100%',
                                backgroundImage: `url(${logoUrl})`,
                                backgroundSize: 'cover',
                                backgroundRepeat: 'no-repeat',
                                backgroundPosition: 'center',
                                opacity: 0.05,
                                zIndex: 0,
                              }}
                            />
                          )}
                          <span
                            style={{
                              position: 'relative',
                              zIndex: 1,
                              fontWeight: 600,
                              fontSize: '14px',
                              color: '#000',
                              textShadow: '0 0 4px white, 0 0 4px white, 0 0 4px white',
                              width: '100%',
                            }}
                          >
                            {bankName || '-'}
                          </span>
                        </div>
                      )
                    },
                  },
                  {
                    title: 'เลขบัญชี',
                    dataIndex: 'account_number',
                    key: 'account_number',
                  },
                  {
                    title: 'ชื่อบัญชี',
                    dataIndex: 'account_name',
                    key: 'account_name',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: PaymentGatewayAccount) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การจัดการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            size="small"
                            icon={<EditOutlined />}
                            onClick={() => handleEditPaymentGateway(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="ยืนยันการลบบัญชี Payment Gateway?"
                            onConfirm={() => handleDeletePaymentGateway(record.id)}
                            okText="ยืนยัน"
                            cancelText="ยกเลิก"
                          >
                            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintPaymentGatewaySummons(record.id)}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintPaymentGatewayEnvelope(record.id)}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                        <Button
                          type="default"
                          size="small"
                          icon={<MailOutlined />}
                          onClick={() => handleOpenEmailModal('payment_gateway', record.id)}
                          block
                          style={{ borderColor: '#1890ff', color: '#1890ff' }}
                        >
                          ส่งอีเมล์
                        </Button>
                        <Button
                          size="small"
                          icon={<HistoryOutlined />}
                          onClick={() => handleShowEmailHistory('payment_gateway', record.id, {
                            documentNumber: record.document_number,
                            providerName: record.provider_name,
                            accountNumber: record.account_number
                          })}
                          block
                          style={{ borderColor: '#722ed1', color: '#722ed1' }}
                        >
                          ประวัติอีเมล์
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>

            <Tabs.TabPane tab={`📱 หมายเลขโทรศัพท์ (${telcoMobileAccounts.length})`} key="telco-mobile-accounts">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddTelcoMobile}
                >
                  เพิ่มหมายเลขโทรศัพท์
                </Button>
              </Space>
              <Table
                dataSource={telcoMobileAccounts}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date',
                    key: 'document_date',
                    render: (date) => formatThaiDate(date),
                  },
                  {
                    title: 'ชื่อผู้ให้บริการ',
                    dataIndex: 'provider_name',
                    key: 'provider_name',
                  },
                  {
                    title: 'หมายเลขโทรศัพท์',
                    dataIndex: 'phone_number',
                    key: 'phone_number',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: TelcoMobileAccount) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การจัดการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            size="small"
                            icon={<EditOutlined />}
                            onClick={() => handleEditTelcoMobile(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="ยืนยันการลบหมายเลขโทรศัพท์?"
                            onConfirm={() => handleDeleteTelcoMobile(record.id)}
                            okText="ยืนยัน"
                            cancelText="ยกเลิก"
                          >
                            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintTelcoMobileSummons(record.id)}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintTelcoMobileEnvelope(record.id)}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                        <Button
                          type="default"
                          size="small"
                          icon={<MailOutlined />}
                          onClick={() => handleOpenEmailModal('telco_mobile', record.id)}
                          block
                          style={{ borderColor: '#1890ff', color: '#1890ff' }}
                        >
                          ส่งอีเมล์
                        </Button>
                        <Button
                          size="small"
                          icon={<HistoryOutlined />}
                          onClick={() => handleShowEmailHistory('telco_mobile', record.id, {
                            documentNumber: record.document_number,
                            providerName: record.provider_name,
                            accountNumber: record.phone_number
                          })}
                          block
                          style={{ borderColor: '#722ed1', color: '#722ed1' }}
                        >
                          ประวัติอีเมล์
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>

            <Tabs.TabPane tab={`🌐 IP Address (${telcoInternetAccounts.length})`} key="telco-internet-accounts">
              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddTelcoInternet}
                >
                  เพิ่ม IP Address
                </Button>
              </Space>
              <Table
                dataSource={telcoInternetAccounts}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date',
                    key: 'document_date',
                    render: (date) => formatThaiDate(date),
                  },
                  {
                    title: 'ชื่อผู้ให้บริการ',
                    dataIndex: 'provider_name',
                    key: 'provider_name',
                  },
                  {
                    title: 'IP Address',
                    dataIndex: 'ip_address',
                    key: 'ip_address',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    render: (reply_status: boolean, record: TelcoInternetAccount) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การจัดการ',
                    key: 'action',
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            size="small"
                            icon={<EditOutlined />}
                            onClick={() => handleEditTelcoInternet(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="ยืนยันการลบ IP Address?"
                            onConfirm={() => handleDeleteTelcoInternet(record.id)}
                            okText="ยืนยัน"
                            cancelText="ยกเลิก"
                          >
                            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintTelcoInternetSummons(record.id)}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintTelcoInternetEnvelope(record.id)}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                        <Button
                          type="default"
                          size="small"
                          icon={<MailOutlined />}
                          onClick={() => handleOpenEmailModal('telco_internet', record.id)}
                          block
                          style={{ borderColor: '#1890ff', color: '#1890ff' }}
                        >
                          ส่งอีเมล์
                        </Button>
                        <Button
                          size="small"
                          icon={<HistoryOutlined />}
                          onClick={() => handleShowEmailHistory('telco_internet', record.id, {
                            documentNumber: record.document_number,
                            providerName: record.provider_name,
                            accountNumber: record.ip_address
                          })}
                          block
                          style={{ borderColor: '#722ed1', color: '#722ed1' }}
                        >
                          ประวัติอีเมล์
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>

            <Tabs.TabPane tab={`👤 ผู้ต้องหาที่เกี่ยวข้อง (${suspects.length})`} key="suspects">

              <Space style={{ marginBottom: 16 }}>
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={handleAddSuspect}
                >
                  เพิ่มผู้ต้องหา
                </Button>
              </Space>
              <Table
                dataSource={suspects}
                loading={loadingDetails}
                rowKey="id"
                size="small"
                rowClassName={(record) => record.reply_status ? 'row-green' : ''}
                columns={[
                  {
                    title: 'เลขหนังสือ',
                    dataIndex: 'document_number',
                    key: 'document_number',
                    render: (value) => value || '-',
                  },
                  {
                    title: 'ลงวันที่',
                    dataIndex: 'document_date',
                    key: 'document_date',
                    render: (date) => formatThaiDate(date),
                  },
                  {
                    title: 'ชื่อผู้ต้องหา',
                    dataIndex: 'suspect_name',
                    key: 'suspect_name',
                    render: (name: string, record: Suspect) => (
                      <Button type="link" onClick={() => showSuspectDetail(record)}>
                        {name}
                      </Button>
                    ),
                  },
                  {
                    title: 'บัตรประชาชน',
                    dataIndex: 'suspect_id_card',
                    key: 'suspect_id_card',
                  },
                  {
                    title: 'ที่อยู่ผู้ต้องหา',
                    dataIndex: 'suspect_address',
                    key: 'suspect_address',
                  },
                  {
                    title: 'สถานะตอบกลับ',
                    dataIndex: 'reply_status',
                    key: 'reply_status',
                    width: 130,
                    render: (reply_status: boolean, record: Suspect) => {
                      if (reply_status) {
                        return <Tag color="green">ตอบกลับแล้ว</Tag>
                      } else {
                        const daysSince = calculateDaysSinceSent(record.document_date)
                        return (
                          <div>
                            <Tag color="red">ยังไม่ตอบกลับ</Tag>
                            <br />
                            <small>ส่งไปแล้ว {daysSince}</small>
                          </div>
                        )
                      }
                    },
                  },
                  {
                    title: 'การดำเนินการ',
                    key: 'action',
                    width: 250,
                    render: (_, record) => (
                      <Space size="small" direction="vertical">
                        <Space size="small">
                          <Button
                            type="link"
                            icon={<EditOutlined />}
                            onClick={() => handleEditSuspect(record)}
                          >
                            แก้ไข
                          </Button>
                          <Popconfirm
                            title="คุณแน่ใจหรือไม่ที่จะลบผู้ต้องหานี้?"
                            onConfirm={() => handleDeleteSuspect(record.id)}
                            okText="ใช่"
                            cancelText="ไม่"
                          >
                            <Button type="link" danger icon={<DeleteOutlined />}>
                              ลบ
                            </Button>
                          </Popconfirm>
                        </Space>
                        <Button
                          type="primary"
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintSuspectSummons(record.id)}
                          block
                        >
                          ปริ้นหมายเรียก
                        </Button>
                        <Button
                          size="small"
                          icon={<PrinterOutlined />}
                          onClick={() => handlePrintSuspectEnvelope(record.id)}
                          block
                        >
                          ปริ้นซองหมายเรียก
                        </Button>
                      </Space>
                    ),
                  },
                ]}
                pagination={false}
              />
            </Tabs.TabPane>
          </Tabs>
        )}
      </Drawer>

      <Modal
        title={`รายละเอียดหมายเรียกผู้ต้องหา - ${selectedSuspect?.suspect_name || ''}`}
        open={suspectDetailOpen}
        onCancel={() => setSuspectDetailOpen(false)}
        footer={[
          <Button key="close" onClick={() => setSuspectDetailOpen(false)}>
            ปิด
          </Button>
        ]}
        width={700}
      >
        {selectedSuspect && (
          <Descriptions column={1} bordered>
            <Descriptions.Item label="เลขหนังสือ">
              {selectedSuspect.document_number || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ลงวันที่">
              {selectedSuspect.document_date_thai || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ชื่อผู้ต้องหา">
              {selectedSuspect.suspect_name}
            </Descriptions.Item>
            <Descriptions.Item label="บัตรประชาชน">
              {selectedSuspect.suspect_id_card || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ที่อยู่ผู้ต้องหา">
              {selectedSuspect.suspect_address || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="กำหนดให้มาพบ">
              {selectedSuspect.appointment_date_thai || selectedSuspect.appointment_date || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="สถานีตำรวจ">
              {selectedSuspect.police_station || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="จังหวัด">
              {selectedSuspect.police_province || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ที่อยู่สถานีตำรวจ">
              {selectedSuspect.police_address || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="สถานะตอบกลับ">
              {selectedSuspect.reply_status ? (
                <Tag color="green">ตอบกลับแล้ว</Tag>
              ) : (
                <Tag color="red">ยังไม่ตอบกลับ</Tag>
              )}
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>

      <Modal
        title="รายละเอียดบัญชีปลายทาง"
        open={cfrDetailVisible}
        onCancel={() => setCfrDetailVisible(false)}
        footer={[
          <Button key="close" onClick={() => setCfrDetailVisible(false)}>
            ปิด
          </Button>
        ]}
        width={600}
      >
        {selectedCfrAccount && (
          <Descriptions column={1} bordered>
            <Descriptions.Item label="ธนาคาร">
              {selectedCfrAccount.to_bank_short_name || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="เลขบัญชี">
              {selectedCfrAccount.to_account_no || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ชื่อบัญชี">
              {selectedCfrAccount.to_account_name || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ประเภทบัตร (to_id_type)">
              {selectedCfrAccount.to_id_type || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="เลขบัตร (to_id)">
              {selectedCfrAccount.to_id || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ชื่อ-นามสกุล">
              {selectedCfrAccount.first_name && selectedCfrAccount.last_name 
                ? `${selectedCfrAccount.first_name} ${selectedCfrAccount.last_name}`
                : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="เบอร์โทรศัพท์ (phone_number)">
              {selectedCfrAccount.phone_number || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ประเภท PromptPay (promptpay_type)">
              {selectedCfrAccount.promptpay_type || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="รหัส PromptPay (promptpay_id)">
              {selectedCfrAccount.promptpay_id || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="สถานะบัญชี">
              {selectedCfrAccount.to_account_status || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="วันเปิดบัญชี">
              {selectedCfrAccount.to_open_date || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="วันปิดบัญชี">
              {selectedCfrAccount.to_close_date || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="ยอดเงินคงเหลือ">
              {selectedCfrAccount.to_balance 
                ? Number(selectedCfrAccount.to_balance).toLocaleString('th-TH', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  }) + ' ฿'
                : '-'}
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>

      <Modal
        title={`แผนผังเส้นทางการเงิน - ${selected?.case_number || ''}`}
        open={flowChartVisible}
        onCancel={() => setFlowChartVisible(false)}
        footer={null}
        width="90%"
        style={{ top: 20 }}
      >
        <CfrFlowChart 
          records={cfrRecords}
          victimName={selected?.complainant}
        />
      </Modal>

      <BankAccountFormModal
        visible={bankModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingBank}
        onClose={handleBankModalClose}
      />

      <NonBankAccountFormModal
        visible={nonBankModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingNonBank}
        onClose={handleNonBankModalClose}
      />

      <PaymentGatewayAccountFormModal
        visible={paymentGatewayModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingPaymentGateway}
        onClose={handlePaymentGatewayModalClose}
      />

      <TelcoMobileAccountFormModal
        visible={telcoMobileModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingTelcoMobile}
        onClose={handleTelcoMobileModalClose}
      />

      <TelcoInternetAccountFormModal
        visible={telcoInternetModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingTelcoInternet}
        onClose={handleTelcoInternetModalClose}
      />

      <SuspectFormModal
        visible={suspectModalVisible}
        criminalCaseId={selected?.id || 0}
        editingRecord={editingSuspect}
        onClose={handleSuspectModalClose}
      />

      <EmailConfirmationModal
        visible={emailModalVisible}
        onCancel={() => setEmailModalVisible(false)}
        onConfirm={handleSendEmail}
        accountType={emailAccountType}
        providerName={emailProviderName}
        documentNumber={emailDocumentNumber}
        defaultEmail={emailDefaultEmail}
        accountNumber={emailAccountNumber}
        phoneNumber={emailPhoneNumber}
        ipAddress={emailIpAddress}
      />

      <EmailHistoryModal
        visible={emailHistoryVisible}
        onClose={() => setEmailHistoryVisible(false)}
        accountType={historyAccountType}
        accountId={historyAccountId}
        accountInfo={historyAccountInfo}
      />

      <style>{`
        .row-red {
          background-color: #fff2f0 !important;
        }
        .row-green {
          background-color: #f6ffed !important;
        }
        .row-closed-case {
          background-color: #f6ffed !important;
        }
      `}</style>
    </div>
  )
}