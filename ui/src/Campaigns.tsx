import Navbar from "./Navbar"
import './App.css';
import { AddCampaignEventReq, AddCampaignGigReq, AddCampaignReq, Campaign, CampaignEvent, CampaignGig, CharacterShort, addCampaign, addCampaignEvent, addCampaignGig, addEventCharacter, addGigCharacter, completeGig, fetchCampaignEvents, fetchCampaignGigs, fetchCampaigns, listCharacters, sortedCharacters } from "./CyberClient";
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
    events: CampaignEvent[]
    setEvents: (events: CampaignEvent[]) => void
}

interface AddEventProps {
    campaignId: number
    setEvents: (events: CampaignEvent[]) => void
}

const resolveCharacterInfos = (characters: CharacterShort[]) =>
    characters.map(c => `${c.name} (${c.role})`).join(', ')


const CampaignEvents = ({events, setEvents}: CampaignEventsProps) => {
    const [characters, setCharacters] = useState<CharacterShort[]>([])

    const filteredCharacters = (e: CampaignEvent) => 
        sortedCharacters(characters).filter(c => !e.characters.map(ec => ec.id).includes(c.id))
        
    useEffect(() => {
       listCharacters().then(setCharacters)
    }, [])

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
                        <td>{resolveCharacterInfos(e.characters)}</td>
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
        info,
    }

    const isValid = info !== undefined && info !== ''
    
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
                <td><button disabled={!isValid} onClick={() => addCampaignEvent(campaignId, addReq).then(() => fetchCampaignEvents(campaignId).then(setEvents))}>Add</button></td>
            </tr>
        </table>
    )
}

interface CampaignGigsProps {
    gigs: CampaignGig[]
    setGigs: (events: CampaignGig[]) => void
}
const CampaignGigs = ({gigs, setGigs}: CampaignGigsProps) => {
    const [characters, setCharacters] = useState<CharacterShort[]>([])

    const filteredCharacters = (g: CampaignGig) => 
        sortedCharacters(characters).filter(c => !g.characters.map(gc => gc.id).includes(c.id))

        useEffect(() => {
            listCharacters().then(setCharacters)
         }, [])

    return(
        <table>
            <tr>
                <th>id</th>
                <th>Gig name</th>
                <th>Gig info</th>
                <th>Characters</th>
                <th>Add character</th>
                <th>Complete gig</th>
            </tr>
            {gigs.map(g => {
                return (
                    <tr>
                        <td>{g.id}</td>
                        <td>{g.name}</td>
                        <td>
                            <textarea value={g.info ?? ''} readOnly={true}/>
                        </td>
                        <td>{resolveCharacterInfos(g.characters)}</td>
                        <td>
                            <select>
                                {filteredCharacters(g).map(c => 
                                    <option value={c.id} onClick={() => addGigCharacter(g.id, c.id).then(setGigs)}>{c.name} ({c.role})</option>
                                )}
                            </select>
                        </td>
                        <td>
                            <button disabled={g.isCompleted} onClick={() => completeGig(g.id).then(() => fetchCampaignGigs(g.campaignId).then(setGigs))}>
                                Complete
                            </button>
                        </td>
                    </tr>
                )
            })}
           
        </table>
    )
}

interface AddGigProps {
    campaignId: number
    setGigs: (g: CampaignGig[]) => void
}

const AddCampaignGig = ({campaignId, setGigs}: AddGigProps) => {
    const [name, setName] = useState<string>('')
    const [info, setInfo] = useState<undefined | string>(undefined)
    const isValid = name !== ''
    const addReq: AddCampaignGigReq = {
        name,
        info,
    }
    
    return(
        <table>
            <tr>
                <th>Gig name</th>
                <th>Gig info</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>
                    <input type='text' value={name} onChange={e => {
                            e.preventDefault()
                            setName(e.target.value)
                        }}
                    />
                </td>
                <td>
                    <textarea onChange={e => {
                        e.preventDefault()
                        setInfo(e.target.value)
                    }}/>
                </td>
                <td>
                    <button disabled={!isValid} onClick={() => addCampaignGig(campaignId, addReq).then(() => fetchCampaignGigs(campaignId).then(setGigs))}>Add</button></td>
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

    return( 
        <div className="main">
            <Navbar />
            <h1>Campaigns</h1>
            <SelectedCampaignInfo />
            <Hideable text='campaigns' props={<CampaignTable campaigns={campaigns} setSelectedCampaign={setSelectedCampaign}/>}/>
            <Hideable text='campaign form' props={<AddCampaign updateCampaigns={updatecampaignsFn}/>} />
            {selectedCampaign && <Hideable text='campaign events' props={<CampaignEvents events={events} setEvents={setEvents} />}/>}
            {selectedCampaign && <Hideable text='campaign event form' props={<AddCampaignEvent setEvents={setEvents} campaignId={selectedCampaign.id} />}/>}
            {selectedCampaign && <Hideable text='campaign gigs' props={<CampaignGigs gigs={gigs} setGigs={setGigs}/>}/>}
            {selectedCampaign && <Hideable text='campaign gig form' props={<AddCampaignGig campaignId={selectedCampaign.id} setGigs={setGigs}/>}/>}
        </div>
    )
}

export default Campaigns