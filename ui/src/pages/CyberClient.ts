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

const postDataAs = <T, >(path: string, data: any): Promise<T> => 
    postData(path, data).then(res => {
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
    Thrown = 'thrown',
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
    skill: string
}

export interface Character {
    id: number
    name: string
    role: string
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
}

export const getCharacter = (name: string) =>
    fetchData(`${pathBase}/char?name=${name}`).then(res => res as Character)

export interface RollReq {
    numberOfDice: number
    dDie: number
}
export const rollDice = (r: RollReq) => 
    postDataAs<number>(`${pathBase}/roll`, r)


export const listSkills = () => 
    fetchDataAs<Skill[]>(`${pathBase}/list-skills`)
 
export interface RollSkillReq {
    charId: number
    skillId: number
    addedLuck: number
}
    //TODO: make POST with params
export const rollSkill = (roll: RollSkillReq) =>
    postDataAs<number>(`${pathBase}/roll-skill`, roll)

export enum AttackType {
    Single = 'single',
    Burst = 'burst',
    FullAuto = 'full auto',
    Melee = 'melee'
}

interface WeaponReq {
    weaponId: number
}

export interface AttackReq extends WeaponReq {
    charId: number
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

export interface LvlUpReq {
    charId: number
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

export const createCharacter = (c: CreateCharacterReq) =>
    postDataAs<Log[]>(`${pathBase}/create-character`, c)

export interface UpdateIPReq {
    charId: number
    ipAmount: number
}

export const updateIP = (ipReq: UpdateIPReq) => 
    postDataAs<Log[]>(`${pathBase}/save-ip`, ipReq)

    /** 
     character_id, dice=None, die=None, divide_by=None, bonus=0, weapon_name=None, clip_size=None, rof=None,
    humanity_cost=None, weapon_t=None, wa=None, con=None, weight=None, reliability=None, effect_radius=None
    */
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

export interface AddWeaponReq {
    charId: number
    item: string
    dice: number
    die: number
    divideBy: number
    dmgBonus: number
    clipSize: number
    wa: number
    humanityCost: number
    effectRadius: number
    weaponType: WeaponType
    con: Con
    reliability: Reliability
}

export const addWeapon = (a: AddWeaponReq) =>
    postDataAs<Log[]>(`${pathBase}/add-weapon`, a)

