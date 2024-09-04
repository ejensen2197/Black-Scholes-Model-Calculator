import React from 'react';
import '../index.css';

const Inputs: React.FC = () => {

    return (
        <div className='flex flex-col w-1/4 h-screen bg-gray-700 pt-10'>
                <div className='text-center'>
                    <h2 className='text-white text-3xl mt-2'>Inputs</h2>
                </div>
                <div className='m-4 flex flex-col'>
                    <h6 className='lbl'>Ticker Symbol:</h6>
                    <div className='flex flex-row'>
                        <input className="px-4 py-2 border-none bg-gray-800 text-white rounded-md focus:outline-none" value='XYZ' /> 
                    </div>    
                </div>
                <div className='m-4 flex flex-col'>
                    <h6 className='lbl'>Strike Price:</h6>
                    <div className='flex flex-row'>
                        <input className='inpt' value='100.00' />
                        <button className='add-sub-button add-button'>+</button>
                        <button className='add-sub-button sub-button'>-</button>
                    </div>
                </div>
                <div className='m-4 flex flex-col'>
                    <h6 className='lbl'>Expiration Date:</h6>
                    <div className='flex flex-row'>
                        <input className='inpt' value='09/20/24' />
                        <button className='add-sub-button add-button'>+</button>
                        <button className='add-sub-button sub-button'>-</button>
                    </div>
                </div>
                <button className='bg-green-400 rounded-md mx-20 mb-2 py-2 hover:bg-green-500'>Run</button>
            </div>
    )
}

export default Inputs;