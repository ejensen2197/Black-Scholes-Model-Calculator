import React from 'react';
import Inputs from '../components/inputs';
import BlackScholes from '../components/black-scholes';
import '../index.css';
const Home: React.FC = () => {

    return (
        <div className='bg-slate-900 flex flex-row'>
            <Inputs />
            <BlackScholes />
            
            
        </div>
    )
}

export default Home;