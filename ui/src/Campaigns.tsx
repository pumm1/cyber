import Navbar from "./Navbar"
import './App.css';
import { Campaign, fetchCampaigns } from "./CyberClient";
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

const AddCampaign = ({}) => {
    const [name, setName] = useState('')
    const [info, setInfo] = useState<string | undefined>(undefined)

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
                <td><button>Add</button></td>
            </tr>
        </table>
    )
}


const Campaigns = ({}) => {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])

    useEffect(() => {
        fetchCampaigns().then(setCampaigns)
    }, [])

    return( 
        <div className="main">
            <Navbar />
            <h1>Campaigns</h1>
            <Hideable text='campaigns' props={<CampaignTable campaigns={campaigns}/>}/>
            <Hideable text='campaign form' props={<AddCampaign />} />
        </div>
    )
}

export default Campaigns