const pathBase = "http://127.0.0.1:5000" //TODO: some env?

const fetchData = (path: string) =>
    fetch(path).then(res => res.json())

const fetchDataAs = <T,>(path: string) =>
    fetchData(path).then(res => res as T)

const postData = <T, >(path: string, data: any) => {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }

    return fetch(path, requestOptions).then(res => {
        console.log(`.... POST RESPONSE: ${JSON.stringify(res)}`)
        
        return res.json() as T
    })
}

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
export const isGun = (w: WeaponType): Boolean =>
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
    bodyTypeModifier: string
    btm?: number //TODO in backend
    woundState: string
    skills: CharacterSkill[]
    armor: Armor[]
    weapons: Weapon[]
    sp: CharacterSP
}

export const getCharacter = (name: string) =>
    fetchData(`${pathBase}/char?name=${name}`).then(res => res as Character)

export const rollDice = () => 
    fetchData(`${pathBase}/roll`)


export const listSkills = () => 
    fetchDataAs<Skill[]>(`${pathBase}/list-skills`)
 
export interface RollSkillReq {
    charId: number
    skillId: number
    addedLuck: number
}
    //TODO: make POST with params
export const rollSkill = (roll: RollSkillReq) =>
    postData<number>(`${pathBase}/roll-skill`, roll)

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
}

export const attack = (attack: AttackReq) =>
    postData<string[]>(`${pathBase}/attack`, attack)

export interface ReloadReq extends WeaponReq {
    shots: number
}

export const reload = (reload: ReloadReq) => 
    postData<string[]>(`${pathBase}/reload`, reload)
