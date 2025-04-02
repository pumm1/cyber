import Navbar from "./Navbar"
import { AddCampaignEventReq, AddCampaignGigReq, AddCampaignReq, Campaign, CampaignEvent, CampaignGig, CharacterShort, GigStatus, addCampaign, addCampaignEvent, addCampaignGig, addEventCharacter, addGigCharacter, deleteEventCharacter, deleteGigCharacter, fetchCampaignEvents, fetchCampaignGigs, fetchCampaigns, listCharacters, sortedCharacters, updateCampaignInfo, updateEventInfo, updateGigInfo, updateGigStatus } from "./CyberClient";
import { useEffect, useState } from "react";
import Hideable from "./Hideable";
import { Button, TextArea } from "./Common";

import './MainPage.css'
import './Campaigns.css'
import { CrtEffect } from "./MainPage";
import MindMap from "./MindMap/MindMap";

interface ListedCharactersProps {
    characters: CharacterShort[]
    onDelete: (cId: number) => Promise<Boolean> 
}

const ListedCharacters = ({ characters, onDelete }: ListedCharactersProps) => 
    <div className='characters'>
        {characters.map(c => <div className='character'>{`${c.name} (${c.role})`} <Button label='X' onClick={() => onDelete(c.id).then()} /></div>)}
    </div>


interface CampaingRowProps {
    campaign: Campaign
    setSelectedCampaign: (c: Campaign) => void
    updateCampaigns: () => Promise<void>
    selectedCampaignId?: number
}


const CampaignRow = ({ campaign, setSelectedCampaign, updateCampaigns, selectedCampaignId }: CampaingRowProps) => {
    const [allowEdit, setAllowedit] = useState(false)
    const [info, setInfo] = useState(campaign.info)
    const editIsvalid: boolean = allowEdit && campaign.info !== info
    return(
        <tr key={campaign.id}>
            <td>{campaign.name}</td>
            <td>
                <TextArea placeholder='Describe campaign somehow' value={info} setValue={setInfo} variant="resizeable" readOnly={!allowEdit}/>
            </td>
            <td>
                <input type='checkbox' checked={allowEdit} onChange={() => setAllowedit(!allowEdit)}/>
            </td>
            <td>
                <Button label='Select' disabled={selectedCampaignId === campaign.id} onClick={() => setSelectedCampaign(campaign)}/>
                <Button variant='LessSpaceLeft' label='Update' disabled={!editIsvalid} onClick={() => updateCampaignInfo(campaign.id, info).then(() => fetchCampaigns().then(updateCampaigns))}/>
            </td>
        </tr>
    )
}

interface CampaignTableProps {
    selectedCampaignId?: number
    campaigns: Campaign[]
    setSelectedCampaign: (c: Campaign) => void
    updateCampaigns: () => Promise<void>
}

const CampaignTable = ({ campaigns, setSelectedCampaign, updateCampaigns, selectedCampaignId }: CampaignTableProps) => {
    return (
        <table>
            <tr>
                <th>Campaign</th>
                <th>Info</th>
                <th>Edit</th>
                <th>Action</th>
            </tr>
        {campaigns.map(c => <CampaignRow selectedCampaignId={selectedCampaignId} campaign={c} setSelectedCampaign={setSelectedCampaign} updateCampaigns={updateCampaigns}/>)}
        </table>
    )
}

interface AddCampaingProps {
    updateCampaigns: () => Promise<void>
}

const AddCampaign = ({updateCampaigns}: AddCampaingProps) => {
    const [name, setName] = useState<undefined | string>(undefined)
    const [info, setInfo] = useState<string | undefined>(undefined)
    const addCampaingReq: AddCampaignReq  = {
        name: name ?? '',
        info
    }

    const emptyForm = () => {
        setName('')
        setInfo('')
    }

    const isValid: boolean = name !== ''

    const addCampaignFn = () =>
        addCampaign(addCampaingReq).then(() => updateCampaigns().then(() => emptyForm()))

    return(
        <table>
            <tr>
                <th>Name</th>
                <th>Info</th>
                <th>Action</th>
            </tr>
            <tr>
                <td><input placeholder='<Campaign name>' value={name} onChange={e => setName(e.target.value)}/></td>
                <td>
                    <TextArea placeholder='Describe campaign somehow' value={info} setValue={setInfo} variant="resizeable"/>
                </td>
                <td><Button label='Add' disabled={!isValid} onClick={() => addCampaignFn()} /></td>
            </tr>
        </table>
    )
}

interface EventRowProps {
    event: CampaignEvent,
    allCharacters: CharacterShort[]
    setEvents: (e: CampaignEvent[]) => void
}

const EventRow = ({event, allCharacters, setEvents}: EventRowProps) => {
    const [allowEdit, setAllowedit] = useState(false)
    const [info, setInfo] = useState(event.info)
    const editIsValid: boolean = allowEdit && event.info !== info

    const updateEvents = () =>
        fetchCampaignEvents(event.campaignId).then(setEvents)

    const deleteCharacter = (c: number) =>
        deleteEventCharacter(event.id, c).then(() => updateEvents().then(() => true))
    
    return (
        <tr>
            <td>{event.sessionNumber}</td>
            <td>
                <TextArea placeholder='Describe event somehow' value={info} setValue={setInfo} variant="resizeable" readOnly={!allowEdit}/>
            </td>
            <td>
                <input type='checkbox' checked={allowEdit} onClick={() => setAllowedit(!allowEdit)}/>
                <Button label='Edit info' disabled={!editIsValid} onClick={() => updateEventInfo(event.id, info).then(() => updateEvents())}/>
            </td>
            <td><ListedCharacters characters={event.characters} onDelete={deleteCharacter}/></td>
            <td>
                <select>
                    {allCharacters.map(c => 
                        <option value={c.id} onClick={() => addEventCharacter(event.id, c.id).then(setEvents)}>{c.name} ({c.role})</option>
                    )}
                </select>
            </td>
        </tr>
    )
}

interface CampaignEventsProps {
    events: CampaignEvent[]
    setEvents: (events: CampaignEvent[]) => void
}

interface AddEventProps {
    campaignId: number
    setEvents: (events: CampaignEvent[]) => void
    maxSession?: number
}

const CampaignEvents = ({events, setEvents}: CampaignEventsProps) => {
    const [characters, setCharacters] = useState<CharacterShort[]>([])
    const [showFilter, setShowFilter] = useState(false)
    const [sessionFilter, setSessionFilter] = useState<undefined | number>(undefined)

    const filteredCharacters = (e: CampaignEvent) => 
        sortedCharacters(characters).filter(c => !e.characters.map(ec => ec.id).includes(c.id))
        
    useEffect(() => {
       listCharacters().then(setCharacters)
    }, [])

    const filteredEvents = () =>
        showFilter && sessionFilter !== undefined ? events.filter(e => e.sessionNumber === sessionFilter) : events

    return (
        <div>
            Show session filter {<input type='checkbox' checked={showFilter} onChange={() => setShowFilter(!showFilter)}/>}       
            {showFilter && 
                <input value={sessionFilter} type='number' onChange={e => {
                        e.preventDefault()
                        const value = parseInt(e.target.value)
                        setSessionFilter(value)
                    }}
                />
            }     
            <table>
                <tr>
                    <th>Session</th>
                    <th>Event info</th>
                    <th>Edit</th>
                    <th>Characters</th>
                    <th>Add character</th>
                </tr>
                {filteredEvents().map(e => {
                    return (
                        <EventRow event={e} setEvents={setEvents} allCharacters={filteredCharacters(e)} />
                    )
                })}
            
            </table>
        </div>
    )
}

const AddCampaignEvent = ({campaignId, setEvents, maxSession}: AddEventProps) => {
    const [sessionNumber, setSessionNumber] = useState<undefined | number>(maxSession)
    const [info, setInfo] = useState<undefined | string>(undefined)
    const addReq: AddCampaignEventReq = {
        sessionNumber: sessionNumber ?? 1,
        info,
    }

    const emptyForm = () => {
        setInfo('')
    }

    const isValid = (info !== undefined && info !== '') && (sessionNumber !== undefined)
    
    return(
        <table>
            <tr>
                <th>Event info</th>
                <th>Session</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>
                    <TextArea placeholder='Describe event somehow' value={info} setValue={setInfo} variant="resizeable"/>
                </td>
                <td>
                    <input value={sessionNumber} type='number' onChange={e => {
                        e.preventDefault()
                        
                        setSessionNumber(parseInt(e.target.value))
                    }}/>
                </td>
                <td>
                    <Button label='Add' disabled={!isValid} onClick={() =>  addCampaignEvent(campaignId, addReq).then(() => fetchCampaignEvents(campaignId).then(setEvents)).then(() => emptyForm())}/>
                </td>
            </tr>
        </ table>
    )
}

const gigStatusLabel = (status: GigStatus) =>
    status === GigStatus.NotStarted ? 'Not started' : status


interface GigRowProps {
    gig: CampaignGig,
    setGigs: (g: CampaignGig[]) => void
    allCharacters: CharacterShort[]
}

const gigIsOver = (g: CampaignGig) =>
    g.status === GigStatus.Done || g.status === GigStatus.Failed


const GigRow = ({gig, setGigs, allCharacters}: GigRowProps) => {
    const [info, setInfo] = useState(gig.info)
    const editIsValid: boolean = gig.info !== info

    const fetchAndUpdategigs = () =>
        fetchCampaignGigs(gig.campaignId).then(setGigs) 

    const deleteCharacter = (c: number) =>
        deleteGigCharacter(gig.id, c).then(() => fetchAndUpdategigs()).then(() => true)
    
    return (
        <tr>
            <td>{gig.id}</td>
            <td>{gig.name}</td>
            <td>
                {gigStatusLabel(gig.status)}
            </td>
            <td>
                <TextArea placeholder='Describe gig somehow' readOnly={true} value={gig.info} setValue={setInfo} variant="resizeable"/>
            </td>
            <td>
                <TextArea placeholder='Describe gig somehow' value={info} setValue={setInfo} readOnly={false} variant="resizeable"/>
            </td>
            <td>
                <Button label='Edit info' disabled={!editIsValid} onClick={() => updateGigInfo(gig.id, info).then(() => fetchAndUpdategigs())}/>
            </td>
            <td><ListedCharacters characters={gig.characters} onDelete={deleteCharacter}/></td>
            <td>
                <select>
                    {allCharacters.map(c => 
                        <option value={c.id} onClick={() => addGigCharacter(gig.id, c.id).then(setGigs)}>{c.name} ({c.role})</option>
                    )}
                </select>
            </td>
            <td>
                <Button label='Start' disabled={gig.status !== GigStatus.NotStarted} onClick={() => updateGigStatus(gig.id, GigStatus.Started).then(() => fetchAndUpdategigs())}/>
                <Button variant='LessSpaceLeft' label='Complete' disabled={gigIsOver(gig)} onClick={() => updateGigStatus(gig.id, GigStatus.Done).then(() => fetchAndUpdategigs())}/>
                <Button variant='LessSpaceLeft' label='Failed' disabled={gigIsOver(gig)} onClick={() => updateGigStatus(gig.id, GigStatus.Failed).then(() => fetchAndUpdategigs())}/>
            </td>
        </tr>
    )
}

interface CampaignGigsProps {
    campaignId: number
    gigs: CampaignGig[]
    setGigs: (g: CampaignGig[]) => void
}

const CampaignGigs = ({ campaignId, gigs, setGigs}: CampaignGigsProps) => {
    const [characters, setCharacters] = useState<CharacterShort[]>([])
    const [showCompleted, setShowCompleted] = useState(true)

    const filteredCharacters = (g: CampaignGig) => 
        sortedCharacters(characters).filter(c => !g.characters.map(gc => gc.id).includes(c.id))

    useEffect(() => {
        listCharacters().then(setCharacters)
    }, [])

    const updateGigs = () => { //showCompleted used here for filtering is still pre-updated value 
        Promise.resolve(setShowCompleted(!showCompleted)).then(() => fetchCampaignGigs(campaignId).then(allGigs => setGigs(!showCompleted ? allGigs : allGigs.filter(g => !gigIsOver(g)))))
    }

    return(
        <div>
            Show completed {<input type='checkbox' checked={showCompleted} onChange={() => { 
                updateGigs()
            }} />}
            <table>
                <tr>
                    <th>id</th>
                    <th>Gig name</th>
                    <th>Status</th>
                    <th>Gig info</th>
                    <th>Info update</th>
                    <th>Edit</th>
                    <th>Characters</th>
                    <th>Add character</th>
                    <th>Action</th>
                </tr>
                {gigs.map(g => {
                    return (
                        <GigRow gig={g} setGigs={setGigs} allCharacters={filteredCharacters(g)} />
                    )
                })}
            
            </table>
        </div>
    )
}

interface AddGigProps {
    campaignId: number
    setGigs: (g: CampaignGig[]) => void
}

const AddCampaignGig = ({campaignId, setGigs}: AddGigProps) => {
    const [name, setName] = useState<string>('')
    const [info, setInfo] = useState<undefined | string>(undefined)
    const [status, setStatus] = useState<GigStatus>(GigStatus.NotStarted)
    const isValid = name !== ''
    const addReq: AddCampaignGigReq = {
        name,
        status,
        info,
    }

    const emptyForm = () => {
        setInfo('')
        setName('')
        setStatus(GigStatus.NotStarted)
    }

    
    return(
        <table>
            <tr>
                <th>Gig name</th>
                <th>Status</th>
                <th>Gig info</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>
                    <input placeholder='<Gig name>' type='text' value={name} onChange={e => {
                            e.preventDefault()
                            setName(e.target.value)
                        }}
                    />
                </td>
                <td>
                    <select value={status}>
                        <option onClick={() => setStatus(GigStatus.NotStarted)}>{gigStatusLabel(GigStatus.NotStarted)}</option>
                        <option onClick={() => setStatus(GigStatus.Started)}>{gigStatusLabel(GigStatus.Started)}</option>
                        <option onClick={() => setStatus(GigStatus.Done)}>{gigStatusLabel(GigStatus.Done)}</option>
                        <option onClick={() => setStatus(GigStatus.Failed)}>{gigStatusLabel(GigStatus.Failed)}</option>
                    </select>
                </td>
                <td>
                    <TextArea placeholder='Describe gig somehow' value={info} setValue={setInfo} variant="resizeable"/>
                </td>
                <td>
                    <Button label='Add' disabled={!isValid} onClick={() => addCampaignGig(campaignId, addReq).then(() => fetchCampaignGigs(campaignId).then(setGigs).then(() => emptyForm()))}/>
                </td>
            </tr>
        </table>
    )
}
 
const Campaigns = ({}) => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])
    const updatecampaignsFn = () => fetchCampaigns().then(setCampaigns)
    const [selectedCampaign, setSelectedCampaign] = useState<Campaign | undefined>(undefined)
    const [events, setEvents] = useState<CampaignEvent[]>([])
    const [gigs, setGigs] = useState<CampaignGig[]>([])

    useEffect(() => {
        selectedCampaign && fetchCampaignEvents(selectedCampaign.id).then(setEvents).then(() => fetchCampaignGigs(selectedCampaign.id).then(setGigs))
    }, [selectedCampaign])

    const SelectedCampaignInfo = ({}) => 
        selectedCampaign ? <div>Selected campaign: <b>{selectedCampaign.name}</b></div> : <></>

    useEffect(() => {
        fetchCampaigns().then(setCampaigns)
    }, [])

    useEffect(() => {
        document.title = "Campaigns"
     }, []);
     
     const CampaignEventsAndGigs = ({}) => 
        <>
            {selectedCampaign && <h2>Campaign events</h2>}
            {selectedCampaign && <Hideable text='campaign events' props={<CampaignEvents events={events} setEvents={setEvents} />}/>}
            {selectedCampaign && <Hideable text='campaign event form' props={<AddCampaignEvent maxSession={Math.max(...events.map(e => e.sessionNumber))} setEvents={setEvents} campaignId={selectedCampaign.id} />}/>}
            {selectedCampaign && <h2>Campaign gigs</h2>}
            {selectedCampaign && <Hideable text='campaign gigs' props={<CampaignGigs campaignId={selectedCampaign.id} gigs={gigs} setGigs={setGigs}/>}/>}
            {selectedCampaign && <Hideable text='campaign gig form' props={<AddCampaignGig campaignId={selectedCampaign.id} setGigs={setGigs}/>}/>}
        </>

    return( 
        <div className="main">
            <CrtEffect />
            <Navbar />
            <h2>Campaigns</h2>
            <SelectedCampaignInfo />
            <Hideable text='campaigns' props={<CampaignTable selectedCampaignId={selectedCampaign?.id} campaigns={campaigns} updateCampaigns={updatecampaignsFn} setSelectedCampaign={setSelectedCampaign}/>}/>
            <Hideable text='campaign form' props={<AddCampaign updateCampaigns={updatecampaignsFn}/>} />
            <Hideable text='campaign evens and gigs' props={<CampaignEventsAndGigs />}/>
        </div>
    )
}

export default Campaigns