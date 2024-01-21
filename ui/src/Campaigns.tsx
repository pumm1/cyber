import Navbar from "./Navbar"
import './App.css'
import './Campaigns.css'
import { AddCampaignEventReq, AddCampaignGigReq, AddCampaignReq, Campaign, CampaignEvent, CampaignGig, CharacterShort, GigStatus, addCampaign, addCampaignEvent, addCampaignGig, addEventCharacter, addGigCharacter, fetchCampaignEvents, fetchCampaignGigs, fetchCampaigns, listCharacters, sortedCharacters, updateCampaignInfo, updateEventInfo, updateGigInfo, updateGigStatus } from "./CyberClient";
import { useEffect, useState } from "react";
import Hideable from "./Hideable";

interface ListedcharactersProps {
    characters: CharacterShort[]
}

//TODO: remove functionality
const ListedCharacters = ({ characters }: ListedcharactersProps) => 
    <div className='characters'>
        {characters.map(c => <div className='character'>{`${c.name} (${c.role})`} <button>X</button></div>)}
    </div>


interface CampaingRowProps {
    campaign: Campaign
    setSelectedCampaign: (c: Campaign) => void
}


const CampaignRow = ({ campaign, setSelectedCampaign }: CampaingRowProps) => {
    const [allowEdit, setAllowedit] = useState(false)
    const [info, setInfo] = useState(campaign.info)
    const editIsvalid: boolean = allowEdit && campaign.info !== info
    return(
        <tr key={campaign.id}>
            <td>{campaign.name}</td>
            <td>
                <textarea value={info} readOnly={!allowEdit} onChange={e => {
                    e.preventDefault()
                    setInfo(e.target.value)
                }}/>
            </td>
            <td>
                <input type='checkbox' checked={allowEdit} onChange={() => setAllowedit(!allowEdit)}/>
            </td>
            <td>
                <button className='withLessRightSpace' onClick={() => setSelectedCampaign(campaign)}>Select</button>
                <button disabled={!editIsvalid} className='withLessRightSpace' onClick={() => updateCampaignInfo(campaign.id, info)}>Update</button>
            </td>
        </tr>
    )
}

interface CampaignTableProps {
    campaigns: Campaign[]
    setSelectedCampaign: (c: Campaign) => void
}

const CampaignTable = ({ campaigns, setSelectedCampaign }: CampaignTableProps) => {
    return (
        <table>
            <tr>
                <th>Campaign</th>
                <th>Info</th>
                <th>Edit</th>
                <th>Action</th>
            </tr>
        {campaigns.map(c => <CampaignRow campaign={c} setSelectedCampaign={setSelectedCampaign}/>)}
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

    return(
        <table>
            <tr>
                <th>Name</th>
                <th>Info</th>
                <th>Action</th>
            </tr>
            <tr>
                <td><input placeholder='<Campaign name>' value={name} onChange={e => setName(e.target.value)}/></td>
                <td><textarea placeholder='Describe campaign somehow' value={info} onChange={e => setInfo(e.target.value)}/></td>
                <td><button disabled={!isValid} onClick={e => {
                    e.preventDefault()

                    addCampaign(addCampaingReq).then(() => updateCampaigns().then(() => emptyForm()))
                }}>Add</button></td>
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
    const editIsvalid: boolean = allowEdit && event.info !== info
    
    return (
        <tr>
            <td>{event.sessionNumber}</td>
            <td>
                <textarea value={info} readOnly={!allowEdit} onChange={e => {
                    e.preventDefault()
                    setInfo(e.target.value)
                }}/>
            </td>
            <td>
                <input type='checkbox' checked={allowEdit} onClick={() => setAllowedit(!allowEdit)}/>
                <button disabled={!editIsvalid} onClick={() => updateEventInfo(event.id, info).then(() => fetchCampaignEvents(event.campaignId).then(setEvents))}>
                    Edit info
                </button>
            </td>
            <td><ListedCharacters characters={event.characters}/></td>
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

const resolveCharacterInfos = (characters: CharacterShort[]) =>
    characters.map(c => `${c.name} (${c.role})`).join(', ')


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
                    <textarea placeholder='Describe event somehow' value={info} onChange={e => {
                        e.preventDefault()
                        setInfo(e.target.value)
                    }}/>
                </td>
                <td>
                    <input value={sessionNumber} type='number' onChange={e => {
                        e.preventDefault()
                        
                        setSessionNumber(parseInt(e.target.value))
                    }}/>
                </td>
                <td>
                    <button disabled={!isValid} onClick={() => {
                            addCampaignEvent(campaignId, addReq).then(() => fetchCampaignEvents(campaignId).then(setEvents)).then(() =>   emptyForm())
                        }}>Add
                    </button>
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
    const [allowEdit, setAllowedit] = useState(false)
    const [info, setInfo] = useState(gig.info)
    const editIsvalid: boolean = allowEdit && gig.info !== info

    const fetchAndUpdategigs = () =>
        fetchCampaignGigs(gig.campaignId).then(setGigs) 
    
    
    return (
        <tr>
            <td>{gig.id}</td>
            <td>{gig.name}</td>
            <td>
                {gigStatusLabel(gig.status)}
            </td>
            <td>
                <textarea value={info} readOnly={!allowEdit} onChange={e => {
                    e.preventDefault()
                    setInfo(e.target.value)
                }}/>
            </td>
            <td>
                <input type='checkbox' checked={allowEdit} onClick={() => setAllowedit(!allowEdit)}/>
                <button disabled={!editIsvalid} onClick={() => 
                        updateGigInfo(gig.id, info).then(() => fetchAndUpdategigs())
                    }
                >
                    Edit info
                </button>
            </td>
            <td>{resolveCharacterInfos(gig.characters)}</td>
            <td>
                <select>
                    {allCharacters.map(c => 
                        <option value={c.id} onClick={() => addGigCharacter(gig.id, c.id).then(setGigs)}>{c.name} ({c.role})</option>
                    )}
                </select>
            </td>
            <td>
                <button className='withLessRightSpace' disabled={gig.status !== GigStatus.NotStarted} onClick={() => updateGigStatus(gig.id, GigStatus.Started).then(() => fetchAndUpdategigs())}>
                    Start
                </button>
                <button className='withLessRightSpace' disabled={gigIsOver(gig)} onClick={() => updateGigStatus(gig.id, GigStatus.Done).then(() => fetchAndUpdategigs())}>
                    Complete
                </button>
                <button className='withLessRightSpace' disabled={gigIsOver(gig)} onClick={() => updateGigStatus(gig.id, GigStatus.Failed).then(() => fetchAndUpdategigs())}>
                    Failed
                </button>
            </td>
        </tr>
    )
}

interface CampaignGigsProps {
    gigs: CampaignGig[]
    setGigs: (g: CampaignGig[]) => void
}

const CampaignGigs = ({gigs, setGigs}: CampaignGigsProps) => {
    const [characters, setCharacters] = useState<CharacterShort[]>([])
    const [showCompleted, setShowCompleted] = useState(false)

    const filteredCharacters = (g: CampaignGig) => 
        sortedCharacters(characters).filter(c => !g.characters.map(gc => gc.id).includes(c.id))

    const filteredGigs = () =>!
        !showCompleted ? gigs.filter(g => !gigIsOver(g)) : gigs

    useEffect(() => {
        listCharacters().then(setCharacters)
    }, [])

    return(
        <div>
            Show completed {<input type='checkbox' checked={showCompleted} onChange={() => setShowCompleted(!showCompleted)} />}
            <table>
                <tr>
                    <th>id</th>
                    <th>Gig name</th>
                    <th>Status</th>
                    <th>Gig info</th>
                    <th>Edit</th>
                    <th>Characters</th>
                    <th>Add character</th>
                    <th>Action</th>
                </tr>
                {filteredGigs().map(g => {
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
                    <textarea placeholder='Describe the gig somehow' value={info} onChange={e => {
                        e.preventDefault()
                        setInfo(e.target.value)
                    }}/>
                </td>
                <td>
                    <button disabled={!isValid} onClick={() => addCampaignGig(campaignId, addReq).then(() => fetchCampaignGigs(campaignId).then(setGigs).then(() => emptyForm()))}>Add</button></td>
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

    return( 
        <div className="main">
            <Navbar />
            <h2>Campaigns</h2>
            <SelectedCampaignInfo />
            <Hideable text='campaigns' props={<CampaignTable campaigns={campaigns} setSelectedCampaign={setSelectedCampaign}/>}/>
            <Hideable text='campaign form' props={<AddCampaign updateCampaigns={updatecampaignsFn}/>} />
            {selectedCampaign && <h2>Campaign events</h2>}
            {selectedCampaign && <Hideable text='campaign events' props={<CampaignEvents events={events} setEvents={setEvents} />}/>}
            {selectedCampaign && <Hideable text='campaign event form' props={<AddCampaignEvent maxSession={Math.max(...events.map(e => e.sessionNumber))} setEvents={setEvents} campaignId={selectedCampaign.id} />}/>}
            {selectedCampaign && <h2>Campaign gigs</h2>}
            {selectedCampaign && <Hideable text='campaign gigs' props={<CampaignGigs gigs={gigs} setGigs={setGigs}/>}/>}
            {selectedCampaign && <Hideable text='campaign gig form' props={<AddCampaignGig campaignId={selectedCampaign.id} setGigs={setGigs}/>}/>}
        </div>
    )
}

export default Campaigns