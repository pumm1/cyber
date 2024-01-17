import Navbar from "./Navbar"
import './App.css';
import { AddCampaignEventReq, AddCampaignReq, Campaign, CampaignEvent, CharacterShort, addCampaign, addCampaignEvent, addEventCharacter, fetchCampaignEvents, fetchCampaigns, listCharacters, sortedCharacters } from "./CyberClient";
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
                <td><input value={name} onChange={e => setName(e.target.value)}/></td>
                <td><textarea value={info} onChange={e => setInfo(e.target.value)}/></td>
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
    events: CampaignEvent[]
    setEvents: (events: CampaignEvent[]) => void
}

interface AddEventProps {
    campaignId: number
    setEvents: (events: CampaignEvent[]) => void
}

const CampaignEvents = ({campaignId, events, setEvents}: CampaignEventsProps) => {
    const [characters, setCharacters] = useState<CharacterShort[]>([])

    const filteredCharacters = (e: CampaignEvent) => 
        sortedCharacters(characters).filter(c => !e.characters.map(ec => ec.id).includes(c.id))
        
    useEffect(() => {
        fetchCampaignEvents(campaignId).then(setEvents).then(() => listCharacters().then(setCharacters))
    }, [campaignId])

    return (
        <table>
            <tr>
                <th>id</th>
                <th>Event info</th>
                <th>Characters</th>
                <th>Add character</th>
            </tr>
            {events.map(e => {
                return (
                    <tr>
                        <td>{e.id}</td>
                        <td>
                            <textarea value={e.info ?? ''} readOnly={true}/>
                        </td>
                        <td>{e.characters.map(c => `${c.name} (${c.role})`).join(', ')}</td>
                        <td>
                            <select>
                                {filteredCharacters(e).map(c => 
                                    <option value={c.id} onClick={() => addEventCharacter(e.id, c.id).then(setEvents)}>{c.name} ({c.role})</option>
                                )}
                            </select>
                        </td>
                    </tr>
                )
            })}
           
        </table>
    )
}

const AddCampaignEvent = ({campaignId, setEvents}: AddEventProps) => {
    const [info, setInfo] = useState<undefined | string>(undefined)
    const addReq: AddCampaignEventReq = {
        campaignId,
        info,
    }
    
    return(
        <table>
            <tr>
                <th>Event info</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>
                    <textarea onChange={e => {
                        e.preventDefault()
                        setInfo(e.target.value)
                    }}/>
                </td>
                <td><button onClick={() => addCampaignEvent(addReq).then(() => fetchCampaignEvents(campaignId).then(setEvents))}>Add</button></td>
            </tr>
        </table>
    )
}
 
const Campaigns = ({}) => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])
    const updatecampaignsFn = () => fetchCampaigns().then(setCampaigns)
    const [selectedCampaign, setSelectedCampaign] = useState<Campaign | undefined>(undefined)
    const [events, setEvents] = useState<CampaignEvent[]>([])

    useEffect(() => {
        selectedCampaign && fetchCampaignEvents(selectedCampaign.id).then(setEvents)
    }, [selectedCampaign])

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
            <Hideable text='campaign form' props={<AddCampaign updateCampaigns={updatecampaignsFn}/>} />
            {selectedCampaign && <Hideable text='campaign events' props={<CampaignEvents events={events} setEvents={setEvents} campaignId={selectedCampaign.id}/>}/>}
            {selectedCampaign && <Hideable text='add campaign event' props={<AddCampaignEvent setEvents={setEvents} campaignId={selectedCampaign.id} />}/>}
        </div>
    )
}

export default Campaigns