import Navbar from "./Navbar"
import './App.css';
import { AddCampaignReq, Campaign, addCampaign, fetchCampaigns } from "./CyberClient";
import { useEffect, useState } from "react";
import Hideable from "./Hideable";

interface CampaignTableProps {
    campaigns: Campaign[]
}

const CampaignTable = ({ campaigns }: CampaignTableProps) => {
    return (
        <table>
            <tr>
                <th>Campaign</th>
                <th>Action</th>
            </tr>
        {campaigns.map(c => 
                <tr key={c.id}>
                    <td>{c.name}</td>
                    <td><button>Select</button></td>
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


const Campaigns = ({}) => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])
    const updatecampaignsFn = () => fetchCampaigns().then(setCampaigns)

    useEffect(() => {
        fetchCampaigns().then(setCampaigns)
    }, [])

    return( 
        <div className="main">
            <Navbar />
            <h1>Campaigns</h1>
            <Hideable text='campaigns' props={<CampaignTable campaigns={campaigns}/>}/>
            <Hideable text='campaign form' props={<AddCampaign updateCampaigns={updatecampaignsFn}/>} />
        </div>
    )
}

export default Campaigns