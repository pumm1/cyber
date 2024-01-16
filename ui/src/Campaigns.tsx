import Navbar from "./Navbar"
import './App.css';
import { AddCampaignEventReq, AddCampaignReq, Campaign, CampaignEvent, addCampaign, addCampaignEvent, fetchCampaignEvents, fetchCampaigns } from "./CyberClient";
import { useEffect, useState } from "react";
import Hideable from "./Hideable";

interface CampaignTableProps {
    campaigns: Campaign[]
    setSelectedCampaign: (c: Campaign) => void
}

const CampaignTable = ({ campaigns, setSelectedCampaign }: CampaignTableProps) => {
    return (
        <table>
            <tr>
                <th>Campaign</th>
                <th>Action</th>
            </tr>
        {campaigns.map(c => 
                <tr key={c.id}>
                    <td>{c.name}</td>
                    <td><button onClick={() => setSelectedCampaign(c)}>Select</button></td>
                </tr>
            )}
        </table>
    )
}

interface AddCampaingProps {
    updateCampaigns: () => Promise<void>
}

const AddCampaign = ({updateCampaigns}: AddCampaingProps) => {
    const [name, setName] = useState('')
    const [info, setInfo] = useState<string | undefined>(undefined)
    const addCampaingReq: AddCampaignReq  = {
        name,
        info
    }

    return(
        <table>
            <tr>
                <th>Name</th>
                <th>Info</th>
                <th>Action</th>
            </tr>
            <tr>
                <td><input className='inputField' value={name} onChange={e => setName(e.target.value)}/></td>
                <td><input className='inputField' value={info} onChange={e => setInfo(e.target.value)}/></td>
                <td><button onClick={e => {
                    e.preventDefault()

                    addCampaign(addCampaingReq).then(() => updateCampaigns())
                }}>Add</button></td>
            </tr>
        </table>
    )
}

interface CampaignEventsProps {
    campaignId: number
}

const CampaignEvents = ({campaignId}: CampaignEventsProps) => {
    const [events, setEvents] = useState<CampaignEvent[]>([])
    useEffect(() => {
        fetchCampaignEvents(campaignId).then(setEvents)
    }, [])

    return (
        <table>
            <tr>
                <th>id</th>
                <th>info</th>
            </tr>
            <tr>
                {events.map(e => {
                    return (
                        <>
                            <td>{e.id}</td>
                            <td>{e.info ?? ''}</td>
                        </>
                    )
                })}
            </tr>
        </table>
    )
}

const AddCampaignEvent = ({campaignId}: CampaignEventsProps) => {
    const [info, setInfo] = useState<undefined | string>(undefined)
    const [characterIds, setCharacterIds] = useState<number[]>([])
    const addReq: AddCampaignEventReq = {
        campaignId,
        info,
        characterIds
    }
    
    return(
        <table>
            <tr>
                <th>Info</th>
                <th>Characters</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>
                    <input className='inputField' type='text' onChange={e => {
                        e.preventDefault()
                        setInfo(e.target.value)
                    }}/>
                </td>
                <td>SELECTOR TODO</td>
                <td><button onClick={() => addCampaignEvent(addReq)}>Add</button></td>
            </tr>
        </table>
    )
}
 
const Campaigns = ({}) => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])
    const updatecampaignsFn = () => fetchCampaigns().then(setCampaigns)
    const [selectedCampaign, setSelectedCampaign] = useState<Campaign | undefined>(undefined)

    const SelectedCampaignInfo = ({}) => 
        selectedCampaign ? <div>Selected campaign: <b>{selectedCampaign.name}</b></div> : <></>

    useEffect(() => {
        fetchCampaigns().then(setCampaigns)
    }, [])

    return( 
        <div className="main">
            <Navbar />
            <h1>Campaigns</h1>
            <SelectedCampaignInfo />
            <Hideable text='campaigns' props={<CampaignTable campaigns={campaigns} setSelectedCampaign={setSelectedCampaign}/>}/>
            {selectedCampaign && <Hideable text='campaign events' props={<CampaignEvents campaignId={selectedCampaign.id}/>}/>}
            {selectedCampaign && <Hideable text='add campaign event' props={<AddCampaignEvent campaignId={selectedCampaign.id} />}/>}
            <Hideable text='campaign form' props={<AddCampaign updateCampaigns={updatecampaignsFn}/>} />
        </div>
    )
}

export default Campaigns