const pathBase = "http://127.0.0.1:5000" //TODO: some env?

const fetchData = (path: string) =>
    fetch(path).then(res => res.json())

const fetchDataAs = <T,>(path: string) =>
    fetchData(path).then(res => res as T)


const postData = (path: string, data: any) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }

    return fetch(path, requestOptions)
}

const putData = (path: string, data: any) => {
    const requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }

    return fetch(path, requestOptions)
}

const deleteData = (path: string, data: any) => {
    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }

    return fetch(path, requestOptions)
}

const postDataAs = <T, >(path: string, data: any): Promise<T> => 
    postData(path, data).then(res => {
       return res.json() as T
    })

const putDataAs = <T, >(path: string, data: any): Promise<T> => 
    putData(path, data).then(res => {
        return res.json() as T
    })

const deleteDataAs = <T, >(path: string, data: any): Promise<T> => 
    deleteData(path, data).then(res => {
        return res.json() as T
    })


export enum Attribute {
    ATTR = 'ATTR',
    BODY = 'BODY',
    COOL = 'COOL',
    EMP = 'EMP',
    INT = 'INT',
    LUCK = 'LUCK',
    MA = 'MA',
    REF = 'REF',
    TECH = 'TECH'
}

export enum AttributeExtra {
    BTM = 'body_type_modifier',
    InitiativeBonus = 'initiative_bonus'
}

export const attributes = [
    Attribute.ATTR, Attribute.BODY, Attribute.COOL, Attribute.EMP, Attribute.INT, 
    Attribute.LUCK, Attribute.MA, Attribute.REF, Attribute.TECH, AttributeExtra.BTM, AttributeExtra.InitiativeBonus
]

export interface AttributeBonus {
    attribute: Attribute | AttributeExtra
    bonus: number
}

export enum BodyPart {
    Head = 'head',
    Body = 'body',
    L_arm = 'l_arm',
    R_arm = 'r_arm',
    L_leg = 'l_leg',
    R_leg = 'r_leg'
}

export interface Attributes {
    ATTR: number
    BODY: number
    COOL: number
    EMP: number
    INT: number
    LUCK: number
    MA: number
    REF: number
    TECH: number
}

export interface Skill {
    attribute: Attribute
    description: string
    id: number,
    skill: string
}

const stringSortFn = (a: string, b: string) => {
    if(a < b) {
        return -1
    } else if (a > b) {
        return 1
    } else return 0
}

export const sortedSkills = (skills: Skill[]) => 
    skills.sort((a,b) => {
        return stringSortFn(a.skill, b.skill)
    })

export const sortedCharacters = (characters: CharacterShort[]) =>
    characters.sort((a,b) => {
        return stringSortFn(a.name, b.name)
    })

export interface SkillBonus {
    skillId: number
    bonus: number
}

export interface Armor {
    bodyParts: BodyPart[]
    id: number
    item: string
    sp: number
}

export enum WeaponType {
    Melee = 'melee',
    Handgun = 'handgun',
    SMG = 'smg',
    Rifle = 'rifle',
    Thrown = 'throwing',
    Shotgun = 'shotgun',
    Heavy = 'heavy'
}

const guns = [WeaponType.Handgun, WeaponType.SMG, WeaponType.Rifle, WeaponType.Shotgun, WeaponType.Heavy]
export const isGun = (w: WeaponType): boolean =>
    guns.includes(w)


export interface Weapon {
    id: number
    isChrome: boolean
    item: string
    clipSize: number
    shotsLeft: number
    rof: number
    weight: number
    weaponType: WeaponType //TODO: enum
    reliability: string //TODO: enum
    range: number
    pointBlankLimit: number
    closeRangeLimit: number
    midRangeLimit: number
    longRangeLimit: number
    extremeRangeLimit: number
    effectRadius: 0
    diceNum: number
    divideBy: number
    dmg: number
    dmgBonus: number
}

export interface SkillBonus {
    skillId: number
    bonus: number
}

export interface Chrome {
    id: number
    item: string
    description: string
    skillBonuses: SkillBonus[]
}

export interface CharacterSP {
    head: number
    body: number
    l_arm: number
    r_arm: number,
    l_leg: number,
    r_leg: number
}

export interface CharacterSkill {
    attribute: Attribute
    id: number
    lvl: number
    originalLvl: number
    skill: string
}

export interface CharacterShort {
    id: number
    name: string
    role: string
    initiative?: number
}

export interface Character extends CharacterShort{
    specialAbility: string, //TODO: enum?
    specialAbilityLvl: number
    bodyType: string
    attributes: Attributes
    btm: number //TODO in backend
    woundState: string
    dmgTaken: number
    skills: CharacterSkill[]
    armor: Armor[]
    weapons: Weapon[]
    chrome: Chrome[],
    sp: CharacterSP
    reputation: number
    humanity: number
    ip: number
    money: number
}

export const getCharacter = (id: number) =>
    fetchData(`${pathBase}/char?id=${id}`).then(res => res as Character)

export interface RollReq {
    numberOfDice: number
    dDie: number
}
export const rollDice = (r: RollReq) => 
    postDataAs<number>(`${pathBase}/roll`, r)


export const listSkills = () => 
    fetchDataAs<Skill[]>(`${pathBase}/list-skills`)
 
export interface CharacterReq {
    charId: number
}

export interface RollSkillReq extends CharacterReq {
    skillId: number
    addedLuck: number
    roll?: number
    modifier: number
}
    //TODO: make POST with params
export const rollSkill = (roll: RollSkillReq) =>
    postDataAs<Log[]>(`${pathBase}/roll-skill`, roll)

export enum AttackType {
    Single = 'single',
    Burst = 'burst',
    FullAuto = 'full auto',
    Melee = 'melee'
}

interface WeaponReq {
    weaponId: number
}

export interface AttackReq extends WeaponReq, CharacterReq {
    attackType: AttackType
    attackRange: number
    attackModifier: number
    givenRoll: number,
    targets?: number
    shotsFired?: number
}

export enum LogType {
    pos = 'positive',
    neutral = 'neutral',
    neg = 'negative'
}

export interface Log {
    log: string
    logType: LogType
}

export const attack = (attack: AttackReq) =>
    postDataAs<Log[]>(`${pathBase}/attack`, attack)

export interface ReloadReq extends WeaponReq {
    shots: number
}

export const reload = (reload: ReloadReq) => 
    postDataAs<Log[]>(`${pathBase}/reload`, reload)

export const repair = (charId: number) =>
    postDataAs<Log[]>(`${pathBase}/repair-sp`, charId)

export interface LvlUpReq extends CharacterReq {
    skillId: number
    amount: number
}

export const lvlUp = (charId: number, skillId: number) => {
    const lvlUpReq = {
        charId,
        skillId,
        amount: 1
    } 

    return postDataAs<Log[]>(`${pathBase}/lvl-up`, lvlUpReq)
}

export interface HealReq {
    charId: number
    amount: number
}

export const heal = (healReq: HealReq) =>
    postDataAs<Log[]>(`${pathBase}/heal`, healReq)

export interface DmgReq {
    charId: number
    dmg: number
    bodyPart: BodyPart
    isAp?: boolean
    passSp?: boolean
}

export const doDmg = (dmgReq: DmgReq) =>
    postDataAs<Log[]>(`${pathBase}/dmg`, dmgReq)

export interface CreateCharacterReq {
    name: string
    attributes: Attributes
    role: string
    btm: number
    randomize: boolean
}

export interface CreateCharacterRes extends CharacterReq {
    logs: Log[]
}

export const createCharacter = (c: CreateCharacterReq) =>
    postDataAs<CreateCharacterRes>(`${pathBase}/create-character`, c)

export interface UpdateIPReq {
    charId: number
    ipAmount: number
}

export const updateIP = (ipReq: UpdateIPReq) => 
    postDataAs<Log[]>(`${pathBase}/save-ip`, ipReq)

export enum Con {
    Pocket = 'P',
    Jacket = 'J',
    LongJacket = 'L',
    NotHideable =  'N'
}

export enum Reliability {
    VeryReliable = 'VR',
    Standard = 'ST',
    Unreliable = 'UR'
}

export interface AddWeaponReq extends CharacterReq {
    item: string
    dice: number
    die: number
    divideBy: number
    dmgBonus: number
    rof: number
    clipSize: number
    wa: number
    humanityCost: number
    effectRadius: number
    weaponType: WeaponType
    con: Con
    weight: number
    reliability: Reliability
    customRange?: number
}

export const addWeapon = (a: AddWeaponReq) =>
    postDataAs<Log[]>(`${pathBase}/add-weapon`, a)

export interface AddChromeReq extends CharacterReq {
    item: string
    description: string
    attributeBonuses: AttributeBonus[]
    skillBonuses: SkillBonus[]
    humanityCost: number
}

export const addChrome = (c: AddChromeReq) =>
    postDataAs<Log[]>(`${pathBase}/add-chrome`, c)


export interface AddArmorReq extends CharacterReq {
    item: string
    sp: number
    ev: number
    bodyParts: BodyPart[]
    attributeBonuses: AttributeBonus[]
    skillBonuses: SkillBonus[]
    humanityCost: number
} 

export const addArmor = (a: AddArmorReq) =>
    postDataAs<Log[]>(`${pathBase}/add-armor`, a)

export interface RemoveArmorReq extends CharacterReq {
    armorId: number
}

export const removeArmor = (r: RemoveArmorReq) =>
    postDataAs<Log[]>(`${pathBase}/remove-armor`, r)


export interface Initiative {
    charId: number
    name: string
    initiative: number
    current: boolean
}
export const listInitiative = () =>
    fetchDataAs<Initiative[]>(`${pathBase}/list-initiative`)

export interface AddToCombatReq extends CharacterReq {
    initiative: number
}

export const addToCombat = (c: AddToCombatReq) =>
    postDataAs<Log[]>(`${pathBase}/add-to-combat`, c)

export const advanceCombatSeq = () => 
    postDataAs<Log[]>(`${pathBase}/advance-combat-seq`, {})

export const clearCombatSeq = () => 
    postDataAs<Log[]>(`${pathBase}/clear-initiatives`, {})

export interface AddRepReq extends CharacterReq {
    rep: number
    repFor: string
}
export const addReputation = (r: AddRepReq) =>
    postDataAs<Log[]>(`${pathBase}/add-reputation`, r)

export interface RollInitiativeReq extends CharacterReq {
    initiative?: number
}

export const rollInitiative = (r: RollInitiativeReq) =>
    postDataAs<number>(`${pathBase}/roll-initiative`, r)

export interface UpdateMoneyReq extends CharacterReq {
    money: number
}

export const updateMoney = (m: UpdateMoneyReq) => 
    postDataAs<Log[]>(`${pathBase}/update-money`, m)

export interface RemoveWeaponReq extends CharacterReq {
    weaponId: number
}

export const removeWeapon = (w: RemoveWeaponReq) =>
    postDataAs<Log[]>(`${pathBase}/remove-weapon`, w)

export interface RemoveChromeReq extends CharacterReq {
    chromeId: number
}

export const removeChrome = (c: RemoveChromeReq) =>
    postDataAs<Log[]>(`${pathBase}/remove-chrome`, c)

export enum MeleeAttackMethod {
    weapon = 'weapon',
    strike = 'strike',
    kick = 'kick',
    throw = 'throw',
    choke = 'choke',
}
export interface MeleeDmgRollReq extends CharacterReq {
    weaponId: number,
    method: MeleeAttackMethod
}

export const rollMeleeDmg = (m: MeleeDmgRollReq) =>
    postDataAs<Log[]>(`${pathBase}/roll-melee-dmg`, m)

export const listCharacters = () => 
    fetchDataAs<CharacterShort[]>(`${pathBase}/list-characters`)

export const faceOffRoll = (c: CharacterReq) =>
    postDataAs<Log[]>(`${pathBase}/roll-face-off`, c)

export interface RestoreEMPReq extends CharacterReq {
    emp: number
}
export const restoreCharEMP = (e: RestoreEMPReq) =>
    postDataAs<Log[]>(`${pathBase}/restore-emp`, e)

export const stuncheck = (c: CharacterReq) =>
    postDataAs<Log[]>(`${pathBase}/stun-check`, c)

export const deleteCharacter = (c: CharacterReq) =>
    postDataAs<Log[]>(`${pathBase}/delete-character`, c)

export interface UpdateCharNameReq extends CharacterReq {
    name: string
}

export const updateCharacterName = (c: UpdateCharNameReq) => 
    postDataAs<Log[]>(`${pathBase}/update-name`, c)

export interface ManualWeaponRollReq {
    rollTotal: number
    weaponType: WeaponType,
    wa: number,
    attackRange: number,
    targets: number
    shots: number
}

export const manualWeaponRoll = (r: ManualWeaponRollReq) =>
    postDataAs<Log[]>(`${pathBase}/manual-weapon-roll`, r)

export interface AddCampaignReq {
    name: string
    info?: string
}

export interface Campaign extends AddCampaignReq{
    id: number
}

export const fetchCampaigns = () => 
    fetchDataAs<Campaign[]>(`${pathBase}/campaigns`)

export const addCampaign = (c: AddCampaignReq) => 
    postDataAs<Log[]>(`${pathBase}/add-campaign`, c)

export interface CampaignEvent {
    id: number,
    campaignId: number,
    sessionNumber: number,
    characters: CharacterShort[]
    info?: string
}

export interface GigCharacter {
    gigId: number,
    character: CharacterShort
    info?: string
}

export enum GigStatus {
    NotStarted = 'NotStarted',
    Started = 'Started',
    Failed = 'Failed',
    Done = 'Done'
}

export interface CampaignGig {
    id: number,
    campaignId: number,
    name: string,
    status: GigStatus,
    info?: string
}

export const fetchCampaignEvents = (campaignId: number) => 
    fetchDataAs<CampaignEvent[]>(`${pathBase}/campaing-events/${campaignId}`)


export interface AddCampaignEventReq {
    sessionNumber: number
    info?: string
}

export const addCampaignEvent = (campaignId: number, r: AddCampaignEventReq) =>
    postDataAs<boolean>(`${pathBase}/add-campaign-event/${campaignId}`, r)
    
export const addEventCharacter = (eventId: number, characterId: number) =>
    postDataAs<CampaignEvent[]>(`${pathBase}/add-event-character/${eventId}`, characterId)

export interface AddCampaignGigReq {
    name: string
    status: GigStatus
    info?: string
}

export const addCampaignGig = (campaignId: number, r: AddCampaignGigReq) =>
    postDataAs<boolean>(`${pathBase}/add-campaign-gig/${campaignId}`, r)

export interface CampaignGig {
    id: number
    campaignId: number
    name: string
    info?: string
    characters: CharacterShort[]
}

export const addGigCharacter = (gigId: number, characterId: number) =>
    postDataAs<CampaignGig[]>(`${pathBase}/add-gig-character/${gigId}`, characterId)

export const fetchCampaignGigs = (campaignId: number) => 
    fetchDataAs<CampaignGig[]>(`${pathBase}/campaign-gigs/${campaignId}`)


export const updateGigStatus = (gigId: number, status: GigStatus) =>
    putDataAs<Boolean>(`${pathBase}/update-gig-status/${gigId}`, status)

export const updateGigInfo = (gigId: number, info?: string) =>
    putDataAs<Boolean>(`${pathBase}/update-gig-info/${gigId}`, info)

export const updateEventInfo = (eventId: number, info?: string) =>
    putDataAs<Boolean>(`${pathBase}/update-event-info/${eventId}`, info)


export const updateCampaignInfo = (campaignId: number, info?: string) =>
    putDataAs<Boolean>(`${pathBase}/update-campaign-info/${campaignId}`, info)

export const deleteGigCharacter = (gigId: number, characterId: number) =>
    deleteDataAs<Boolean>(`${pathBase}/delete-gig-character/${gigId}`, characterId)

export const deleteEventCharacter = (eventId: number, characterId: number) =>
    deleteDataAs<Boolean>(`${pathBase}/delete-event-character/${eventId}`, characterId)

export enum CharacterStatusType {
    Positive = 'Positive',
    Neutral = 'Neutral',
    Negative = 'Negative'
}
