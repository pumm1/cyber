import React, { useEffect, useState } from 'react'
import './MindMap.css'
import { Campaign, MindMapData, fetchCampaigns, getCampaignMindMap, saveCampaignMindMap } from '../CyberClient'
import { Button, TextArea } from '../Common'
import { CrtEffect } from '../MainPage'
import Navbar from '../Navbar'
import { debounce } from 'lodash'

//TODO: just create child nodes from nodes?
export type MindMapNode = {
    id: string
    title: string
    info: string
    x: number
    y: number
}

//in most projects ID should properly be generated in BE but now just sending id from UI for BE to make id syncing a bit easier
const generateNodeId = (i: number) => 
    `N${i}-${Math.floor(Math.random()*1000)}`

export type Connection = {
    from: string
    to: string
}
  

  type NodeProps = {
    node: MindMapNode
    addNewNode: (n: MindMapNode) => void
    existingNodes: number
    addConnection: (a: MindMapNode, b: MindMapNode) => void
    updateNode: (n: MindMapNode) => void
    removeNode: (id: string) => void
  }
  
  const Node: React.FC<NodeProps> = ({ node, addNewNode, existingNodes, addConnection, updateNode, removeNode }) => {
    const [title, setTitle] = useState(node.title)
    const [info, setInfo] = useState(node.info)
  
    const handleMouseDown = (e: React.MouseEvent) => {
      const offsetX = e.clientX - node.x
      const offsetY = e.clientY - node.y
  
      const handleMouseMove = (moveEvent: MouseEvent) => {
        const newX = moveEvent.clientX - offsetX
        const newY = moveEvent.clientY - offsetY
        updateNode({...node, x: newX, y: newY}) // Update in MindMap state
      }
  
      const handleMouseUp = () => {
        window.removeEventListener('mousemove', handleMouseMove)
        window.removeEventListener('mouseup', handleMouseUp)
      }
  
      window.addEventListener('mousemove', handleMouseMove)
      window.addEventListener('mouseup', handleMouseUp)
    }

    useEffect(() => {
        updateNode({...node, title, info})
    }, [title, info])
  
    return (
      <div
        className="node"
        style={{ left: `${node.x}px`, top: `${node.y}px` }}
        onMouseDown={handleMouseDown}
      >
        <div className="node-title">
          <input value={title} onChange={e => setTitle(e.target.value)} />
        </div>
        <TextArea variant='small' value={info} setValue={setInfo}/>
        <div>
            <Button label='+' onClick={() => {
                const newId = generateNodeId(existingNodes + 1)
                const childNode: MindMapNode = { id: newId, title: '', info: '', x: node.x, y: node.y + 160 }
                Promise.resolve(addNewNode(childNode)).then(() => addConnection(node, childNode))
            }} />
            <Button variant='LessSpaceLeft' label='Remove' onClick={() => removeNode(node.id)} />
        </div>
      </div>
    )
  }
  

const defaultNode = (): MindMapNode => {
    return { id: generateNodeId(Math.floor(Math.random() * 100)), title: 'Root Node', info: '', x: 100, y: 100 }
}


const MindMap = ({ campaignId }: { campaignId: number }) => {
    const [nodes, setNodes] = useState<MindMapNode[]>([defaultNode()])
    const [connections, setConnections] = useState<Connection[]>([])
    const [loading, setLoading] = useState(false)
  
    useEffect(() => {
        setLoading(true)
        getCampaignMindMap(campaignId).then(res => {
            setNodes(res.nodes)
            setConnections(res.connections)
            setLoading(false)
        })
    }, [campaignId])
  
    const saveMindMap = () => {
        setLoading(true)
        saveCampaignMindMap(campaignId, { nodes, connections })
            .then(() => setLoading(false))
    }

    const addConnection = (a: MindMapNode, b: MindMapNode) =>
        setConnections([...connections, { from: a.id, to: b.id }])

    const addNewNode = (n: MindMapNode) => setNodes([...nodes, n])

    const updateNode = (n: MindMapNode) => {
        setNodes(prevNodes =>
            prevNodes.map(node => node.id === n.id ? { ...node, x: n.x, y: n.y, title: n.title, info: n.info } : node)
        )
    }

    const removeNode = (id: string) => {
        setNodes(nodes.filter(n => n.id !== id))
        setConnections(connections.filter(c => c.from !== id && c.to !== id))
    }
  
    return (
        <div>
            <h3>Mind map</h3>
            <Button label='Save' onClick={saveMindMap} /> {loading && 'Loading...'}
            <div className="mind-map" style={{ position: 'relative', width: '100%', height: '100vh' }}>
                <svg className="lines" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 0 }}>
                    {connections.map((connection, index) => {
                        const fromNode = nodes.find(node => node.id === connection.from)
                        const toNode = nodes.find(node => node.id === connection.to)
                        if (!fromNode || !toNode) return null
                        return (
                            <line
                                key={index}
                                x1={fromNode.x + 50} y1={fromNode.y + 25}
                                x2={toNode.x + 50} y2={toNode.y + 25}
                                stroke="black" strokeWidth="2"
                            />
                        )
                    })}
                </svg>
                {nodes.map(node => (
                    <Node
                        key={node.id}
                        node={node}
                        existingNodes={nodes.length}
                        addNewNode={addNewNode}
                        addConnection={addConnection}
                        updateNode={updateNode}
                        removeNode={removeNode}
                    />
                ))}
                <Button label='Add node' onClick={() => addNewNode(defaultNode())} />
            </div>
        </div>
    )
}
  
const MindMapModal = () => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])
    const [selectedCampaign, setSelectedCampaign] = useState<Campaign | undefined>()

    useEffect(() => {
        fetchCampaigns().then(setCampaigns)
    }, [])

    return (
        <div className='main'>
            <CrtEffect />
            <Navbar />
            <div className='mind-map-container'>
                <select onChange={e => setSelectedCampaign(campaigns.find(c => c.id === Number(e.target.value)))}>
                    {campaigns.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
                {selectedCampaign && (
                    <div>
                        <h3>{selectedCampaign.name}</h3>
                        <MindMap campaignId={selectedCampaign.id} />
                    </div>
                )}
            </div>
        </div>
    )
}
  
export default MindMapModal
  
