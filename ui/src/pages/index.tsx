import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"
import Dice from "./Dice"
import SearchCharacter from "./SearchCharacter"
import './index.css'


const IndexPage: React.FC<PageProps> = () => {
  return (
    <div className='main'>
      <h1>Welcome to the NET</h1>
      <div className='container'>
        <Dice/>
        <SearchCharacter/>
      </div>
    </div>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>The NET</title>
