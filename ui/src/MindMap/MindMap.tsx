import React, { useEffect, useRef, useState } from 'react'
import './MindMap.css'
import { MindMapData, getCampaignMindMap, saveCampaignMindMap } from '../CyberClient'
import { Button, TextArea } from '../Common'

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
    moveNode: (id: string, x: number, y: number) => void
    updateNode: (n: MindMapNode) => void
    removeNode: (id: string) => void
  }
  
  const Node: React.FC<NodeProps> = ({ node, addNewNode, existingNodes, addConnection, moveNode, updateNode, removeNode }) => {
    const [title, setTitle] = useState(node.title)
    const [info, setInfo] = useState(node.info)
  
    const handleMouseDown = (e: React.MouseEvent) => {
      const offsetX = e.clientX - node.x
      const offsetY = e.clientY - node.y
  
      const handleMouseMove = (moveEvent: MouseEvent) => {
        const newX = moveEvent.clientX - offsetX
        const newY = moveEvent.clientY - offsetY
        moveNode(node.id, newX, newY) // Update in MindMap state
      }
  
      const handleMouseUp = () => {
        window.removeEventListener('mousemove', handleMouseMove)
        window.removeEventListener('mouseup', handleMouseUp)
      }
  
      window.addEventListener('mousemove', handleMouseMove)
      window.addEventListener('mouseup', handleMouseUp)
    }

    const handleSave = () => {
        updateNode({ ...node, title, info }) // Update the node in state
    }

  
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
            <Button variant='LessSpaceLeft' label='Save (locally)' onClick={() => handleSave()} />
            <Button variant='LessSpaceLeft' label='Remove (locally)' onClick={() => removeNode(node.id)} />
        </div>
      </div>
    )
  }
  
interface MindMapProps {
    campaignId: number
}

const defaultNode: MindMapNode =  { id: generateNodeId(Math.floor(Math.random() * 100)), title: 'Root Node', info: '', x: 100, y: 100 }

const MindMap = ({campaignId}: MindMapProps) => {
    const [mindMap, setMindMap] = useState<MindMapData | undefined>(undefined)

    const [nodes, setNodes] = useState<MindMapNode[]>(mindMap?.nodes ?? [defaultNode])
    const [connections, setConnections] = useState<Connection[]>(mindMap?.connections ?? [])

    useEffect(() => {
        getCampaignMindMap(campaignId).then(res => {
            setMindMap(res)
            setNodes(res.nodes)
            setConnections(res.connections)
        })
    }, [campaignId])
  
    const addConnection = (a: MindMapNode, b: MindMapNode) =>
      setConnections([...connections, { from: a.id, to: b.id }])
  
    const addNewNode = (n: MindMapNode) => setNodes([...nodes, n])
  
    // Move node in global state so lines update dynamically
    const moveNode = (id: string, newX: number, newY: number) => {
      setNodes((prevNodes) =>
        prevNodes.map((node) =>
          node.id === id ? { ...node, x: newX, y: newY } : node
        )
      )
    }

    const mindMapReq: MindMapData = { nodes, connections } 

    const saveMindMap = () => //ehh..
        saveCampaignMindMap(campaignId, mindMapReq).then(() => console.log(`saved`))

    const removeNode = (id: string) => {
        setNodes(nodes.filter(n => n.id !== id))
        setConnections(connections.filter(c => c.from !== id && c.to !== id))
    }        

    const updateNode = (updatedNode: MindMapNode) => {
        setNodes((prevNodes) =>
            prevNodes.map((node) =>
                node.id === updatedNode.id ? { ...node, ...updatedNode } : node
            )
        )
    }
    
  
    return (
      <div>
        <h3>Mind map</h3>
        <Button label='Save mind map to DB' onClick={() => saveMindMap()} />
        <Button variant='MoreSpaceLeft' label='Add new node' onClick={() => addNewNode(defaultNode)} />
        <div className="mind-map" style={{ position: 'relative', width: '100%', height: '100vh' }}>
            {/* Render SVG Lines First (Behind Nodes) */}
            <svg className="lines" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 0 }}>
                {connections.map((connection, index) => {
                const fromNode = nodes.find((node) => node.id === connection.from)
                const toNode = nodes.find((node) => node.id === connection.to)

                if (!fromNode || !toNode) return null

                return (
                    <line
                    key={index}
                    x1={fromNode.x + 50}
                    y1={fromNode.y + 25}
                    x2={toNode.x + 50}
                    y2={toNode.y + 25}
                    stroke="black"
                    strokeWidth="2"
                    />
                )
                })}
            </svg>

            {/* Render Nodes on Top */}
            {nodes.map((node) => (
                <Node 
                    key={node.id} 
                    node={node} 
                    existingNodes={nodes.length} 
                    addNewNode={addNewNode} 
                    addConnection={addConnection} 
                    moveNode={moveNode} 
                    updateNode={updateNode}
                    removeNode={removeNode}
                />
            ))}
        </div>
      </div>
    )
  }
  
  

export default MindMap
