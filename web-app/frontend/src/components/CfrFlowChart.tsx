import { useEffect, useRef } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
  Position,
} from 'reactflow'
import 'reactflow/dist/style.css'

interface CfrFlowChartProps {
  records: any[]
  victimName?: string
}

const CfrFlowChart: React.FC<CfrFlowChartProps> = ({ records, victimName }) => {
  const flowRef = useRef<HTMLDivElement>(null)
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  // สร้าง nodes และ edges จากข้อมูล CFR
  useEffect(() => {
    if (!records || records.length === 0) return

    const accountMap = new Map<string, any>()
    const edgesList: Edge[] = []
    let nodeId = 0

    // Helper: ตรวจสอบว่าเป็นผู้เสียหายหรือไม่
    const checkIsVictim = (accountName: string): boolean => {
      if (!victimName || !accountName) return false
      const cleanVictim = victimName.replace(/^(นาย|นาง|นางสาว|น\.ส\.|Mr\.|Mrs\.)\s*/gi, '').toLowerCase()
      const cleanAccount = accountName.replace(/^(นาย|นาง|นางสาว|น\.ส\.|Mr\.|Mrs\.)\s*/gi, '').toLowerCase()
      return cleanAccount.includes(cleanVictim) || cleanVictim.includes(cleanAccount)
    }

    // เรียงลำดับ records ตามเวลาก่อนเพื่อคำนวณลำดับการโอนของผู้เสียหาย
    const sortedRecords = [...records].sort((a, b) => {
      const dateTimeA = `${a.transfer_date} ${a.transfer_time || '00:00:00'}`
      const dateTimeB = `${b.transfer_date} ${b.transfer_time || '00:00:00'}`
      return dateTimeA.localeCompare(dateTimeB)
    })
    
    // คำนวณลำดับการโอนของผู้เสียหาย
    let victimTransferCount = 0
    const victimTransferSequence = new Map<number, number>()
    
    sortedRecords.forEach((record, idx) => {
      const isFromVictim = checkIsVictim(record.from_account_name)
      if (isFromVictim) {
        victimTransferCount++
        victimTransferSequence.set(idx, victimTransferCount)
      }
    })
    
    // สร้าง unique accounts และนับ connections
    records.forEach((record, index) => {
      // From Account
      const fromKey = `${record.from_bank_short_name}-${record.from_account_no}`
      if (!accountMap.has(fromKey)) {
        const isVictim = checkIsVictim(record.from_account_name)
        accountMap.set(fromKey, {
          id: `node-${nodeId++}`,
          key: fromKey,
          bank: record.from_bank_short_name,
          accountNo: record.from_account_no,
          accountName: record.from_account_name,
          isVictim,
          level: -1,
          incomingCount: 0,
          outgoingCount: 0,
          transfers: [] // เก็บรายการโอนเงิน
        })
      }
      accountMap.get(fromKey).outgoingCount++

      // To Account
      const toKey = `${record.to_bank_short_name}-${record.to_account_no}`
      if (!accountMap.has(toKey)) {
        const isVictim = checkIsVictim(record.to_account_name)
        accountMap.set(toKey, {
          id: `node-${nodeId++}`,
          key: toKey,
          bank: record.to_bank_short_name,
          accountNo: record.to_account_no,
          accountName: record.to_account_name,
          isVictim,
          level: -1,
          incomingCount: 0,
          outgoingCount: 0,
          transfers: [] // เก็บรายการโอนเงิน
        })
      }
      accountMap.get(toKey).incomingCount++
      
      // เก็บข้อมูลการโอนเงินเข้าบัญชีปลายทาง
      accountMap.get(toKey).transfers.push({
        date: record.transfer_date,
        time: record.transfer_time,
        amount: record.transfer_amount
      })
      
      // เก็บลำดับการโอนของผู้เสียหายไว้ในบัญชีปลายทาง
      const isFromVictim = checkIsVictim(record.from_account_name)
      if (isFromVictim) {
        const sortedIndex = sortedRecords.findIndex(r => 
          r.transfer_date === record.transfer_date &&
          r.transfer_time === record.transfer_time &&
          r.from_account_no === record.from_account_no &&
          r.to_account_no === record.to_account_no &&
          r.transfer_amount === record.transfer_amount
        )
        const sequence = victimTransferSequence.get(sortedIndex)
        if (sequence) {
          accountMap.get(toKey).victimTransferSequence = sequence
        }
      }

      // สร้าง Edge (ลบ label ออกจากเส้น)
      const fromNode = accountMap.get(fromKey)
      const toNode = accountMap.get(toKey)
      
      edgesList.push({
        id: `edge-${index}`,
        source: fromNode.id,
        target: toNode.id,
        type: 'smoothstep',
        animated: true,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#1890ff',
        },
        style: { stroke: '#1890ff', strokeWidth: 2 },
      })
    })

    // คำนวณ level แบบ hierarchical ที่ถูกต้อง (BFS - Breadth First Search)
    const calculateLevels = () => {
      // Reset levels
      accountMap.forEach(account => {
        account.level = -1
      })

      // หาบัญชีผู้เสียหาย (ระดับ 0)
      const victimAccounts: any[] = []
      accountMap.forEach(account => {
        if (account.isVictim) {
          account.level = 0
          victimAccounts.push(account)
        }
      })

      // ถ้าไม่มีผู้เสียหาย ให้หาบัญชีที่โอนออกอย่างเดียว (ต้นทาง)
      if (victimAccounts.length === 0) {
        accountMap.forEach(account => {
          if (account.outgoingCount > 0 && account.incomingCount === 0) {
            account.level = 0
            victimAccounts.push(account)
          }
        })
      }

      // BFS: คำนวณ level ของบัญชีอื่นๆ
      const visited = new Set<string>()
      const queue: Array<{accountId: string, level: number}> = []
      
      // เริ่มจากผู้เสียหาย/ต้นทาง
      victimAccounts.forEach(account => {
        queue.push({ accountId: account.key, level: 0 })
        visited.add(account.key)
      })

      while (queue.length > 0) {
        const { accountId, level } = queue.shift()!
        
        // หา edges ที่ออกจาก account นี้
        records.forEach(record => {
          const fromKey = `${record.from_bank_short_name}-${record.from_account_no}`
          const toKey = `${record.to_bank_short_name}-${record.to_account_no}`
          
          if (fromKey === accountId && !visited.has(toKey)) {
            const toAccount = accountMap.get(toKey)
            if (toAccount) {
              toAccount.level = level + 1
              visited.add(toKey)
              queue.push({ accountId: toKey, level: level + 1 })
            }
          }
        })
      }

      // บัญชีที่ยังไม่มี level ให้ใส่ไว้ท้ายสุด
      accountMap.forEach(account => {
        if (account.level === -1) {
          account.level = 99 // ไว้ท้ายสุด
        }
      })
    }
    calculateLevels()

    // จัดเรียงตาม level (บนลงล่าง) และกระจายซ้าย-ขวา
    const accountsByLevel = new Map<number, any[]>()
    accountMap.forEach(account => {
      if (!accountsByLevel.has(account.level)) {
        accountsByLevel.set(account.level, [])
      }
      accountsByLevel.get(account.level)!.push(account)
    })
    
    // เรียงลำดับบัญชีในแต่ละ level ตามเวลาที่โอนเข้า (ซ้ายไปขวา = เก่าไปใหม่)
    accountsByLevel.forEach((accounts) => {
      accounts.sort((a, b) => {
        // ถ้ามีข้อมูลการโอนเข้า ให้เรียงตามเวลา
        if (a.transfers.length > 0 && b.transfers.length > 0) {
          const dateTimeA = `${a.transfers[0].date} ${a.transfers[0].time || '00:00:00'}`
          const dateTimeB = `${b.transfers[0].date} ${b.transfers[0].time || '00:00:00'}`
          return dateTimeA.localeCompare(dateTimeB)
        }
        // ถ้าไม่มีข้อมูลการโอนเข้า ให้เรียงตามชื่อบัญชี
        return (a.accountNo || '').localeCompare(b.accountNo || '')
      })
    })

    const nodesList: Node[] = []
    const nodePositions = new Map<string, { x: number, y: number }>() // เก็บตำแหน่ง node
    
    accountsByLevel.forEach((accounts, level) => {
      accounts.forEach((account, indexInLevel) => {
        const totalInLevel = accounts.length
        const spacing = 280
        const levelHeight = 180
        
        let x: number
        let y = level * levelHeight
        
        if (level <= 1) {
          // Level 0-1: อยู่กึ่งกลาง
          const totalWidth = (totalInLevel - 1) * spacing
          const startX = -totalWidth / 2
          x = startX + (indexInLevel * spacing)
        } else {
          // Level 2+: วางตรงแนวกับบัญชีต้นทาง
          // หาบัญชีต้นทางที่โอนมา
          const incomingEdge = edgesList.find(edge => edge.target === account.id)
          if (incomingEdge) {
            const sourcePos = nodePositions.get(incomingEdge.source)
            if (sourcePos) {
              // วางตรงแนวกับบัญชีต้นทาง
              x = sourcePos.x
            } else {
              // fallback: วางเรียงจากซ้ายไปขวา
              x = -600 + (indexInLevel * spacing)
            }
          } else {
            // ไม่มี incoming edge: วางเรียงจากซ้ายไปขวา
            x = -600 + (indexInLevel * spacing)
          }
        }
        
        // เก็บตำแหน่ง
        nodePositions.set(account.id, { x, y })

        // คำนวณยอดรวมที่โอนเข้า
        const totalReceived = account.transfers.reduce((sum: number, t: any) => sum + (Number(t.amount) || 0), 0)
        const hasTransfers = account.transfers.length > 0

        const logoUrl = account.bank ? `/Bank-icons/${account.bank}.png` : ''
        
        nodesList.push({
          id: account.id,
          type: 'default',
          position: { x, y },
          data: {
            label: (
              <div style={{ 
                padding: '6px', 
                textAlign: 'center',
                position: 'relative',
                overflow: 'hidden'
              }}>
                {/* Logo พื้นหลัง */}
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
                      opacity: account.isVictim ? 0.15 : 0.08,
                      zIndex: 0,
                    }}
                  />
                )}
                
                {/* เนื้อหา */}
                <div style={{ position: 'relative', zIndex: 1 }}>
                  {/* แสดงลำดับการโอนของผู้เสียหาย (ด้านบนสุด) */}
                  {account.victimTransferSequence && (
                    <div style={{ 
                      fontSize: '10px', 
                      color: '#fa8c16',
                      background: '#fff7e6',
                      padding: '4px 8px',
                      borderRadius: 4,
                      marginBottom: 4,
                      fontWeight: 'bold',
                      border: '1px solid #ffa940'
                    }}>
                      ผู้เสียหายโอนครั้งที่ {account.victimTransferSequence}
                    </div>
                  )}
                  
                  {/* แสดงวันเวลาและจำนวนเงินที่รับเข้า */}
                  {hasTransfers && (
                    <div style={{ 
                      fontSize: '9px', 
                      color: account.isVictim ? '#fff' : '#1890ff',
                      background: account.isVictim ? '#389e0d' : '#bae7ff',
                      padding: '3px 6px',
                      borderRadius: 3,
                      marginBottom: 4,
                      fontWeight: 'bold'
                    }}>
                      {account.transfers[0].date} {account.transfers[0].time}
                      {account.transfers.length > 1 && ` (+${account.transfers.length - 1})`}
                      <div>{totalReceived.toLocaleString('th-TH', { maximumFractionDigits: 0 })} ฿</div>
                    </div>
                  )}
                  
                  {/* ข้อมูลบัญชี */}
                  <div style={{ 
                    fontWeight: 'bold', 
                    fontSize: '13px',
                    color: account.isVictim ? '#fff' : '#1890ff',
                    marginBottom: 3,
                    textShadow: account.isVictim ? '0 0 3px rgba(0,0,0,0.3)' : '0 0 3px white'
                  }}>
                    {account.bank || '-'}
                    {account.isVictim && (
                      <div style={{ 
                        fontSize: '9px', 
                        background: '#389e0d',
                        color: 'white',
                        padding: '2px 6px',
                        borderRadius: 3,
                        marginTop: 2
                      }}>
                        ผู้เสียหาย
                      </div>
                    )}
                  </div>
                  <div style={{ 
                    fontSize: '11px', 
                    fontWeight: '500', 
                    marginBottom: 2,
                    textShadow: account.isVictim ? '0 0 2px rgba(0,0,0,0.2)' : 'none'
                  }}>
                    {account.accountNo || '-'}
                  </div>
                  <div style={{ 
                    fontSize: '10px', 
                    color: account.isVictim ? '#fff' : '#666',
                    maxWidth: 160,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                    textShadow: account.isVictim ? '0 0 2px rgba(0,0,0,0.2)' : 'none'
                  }}>
                    {account.accountName || '-'}
                  </div>
                </div>
              </div>
            ),
          },
          style: {
            background: account.isVictim ? '#52c41a' : '#e6f7ff',
            border: account.isVictim ? '3px solid #389e0d' : '2px solid #1890ff',
            borderRadius: 8,
            width: 180,
            boxShadow: account.isVictim ? '0 4px 12px rgba(82, 196, 26, 0.4)' : '0 2px 8px rgba(0, 0, 0, 0.1)',
          },
          sourcePosition: Position.Bottom,
          targetPosition: Position.Top,
        })
      })
    })

    setNodes(nodesList)
    setEdges(edgesList)
  }, [records, victimName, setNodes, setEdges])


  if (records.length === 0) {
    return <div style={{ color: '#999', padding: 20 }}>ไม่มีข้อมูลสำหรับแสดงแผนผัง</div>
  }

  return (
    <div>

      <div 
        ref={flowRef}
        style={{ 
          width: '100%', 
          height: '600px',
          border: '1px solid #d9d9d9',
          borderRadius: 8,
          background: '#fafafa'
        }}
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          attributionPosition="bottom-right"
        >
          <Background />
          <Controls />
          <MiniMap 
            nodeColor={(node) => {
              const isVictim = node.data?.isVictim
              return isVictim ? '#52c41a' : '#1890ff'
            }}
            maskColor="rgba(0, 0, 0, 0.1)"
          />
        </ReactFlow>
      </div>

      <div style={{ marginTop: 16, fontSize: 12, color: '#666' }}>
        <strong>คำอธิบาย:</strong>
        <ul style={{ marginTop: 8, paddingLeft: 20, lineHeight: 1.8 }}>
          <li>🟩 <strong style={{ color: '#52c41a' }}>กรอบสีเขียว</strong> = บัญชีผู้เสียหาย (อยู่บนสุด)</li>
          <li>🟦 กรอบสีน้ำเงิน = บัญชีธนาคารอื่น</li>
          <li>➡️ ลูกศร (บนลงล่าง) = การโอนเงิน (จำนวนเงินแสดงบนลูกศร)</li>
          <li>📊 ชั้นที่ 1 (บน) = บัญชีต้นทาง/ผู้เสียหาย</li>
          <li>📊 ชั้นที่ 2 (กลาง) = บัญชีกลาง (รับและโอนต่อ)</li>
          <li>📊 ชั้นที่ 3 (ล่าง) = บัญชีปลายทาง</li>
          <li>📍 ลากเพื่อเลื่อนตำแหน่ง, Scroll เพื่อ Zoom</li>
        </ul>
      </div>

    </div>
  )
}

export default CfrFlowChart

