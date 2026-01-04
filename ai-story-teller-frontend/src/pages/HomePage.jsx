import React from 'react'
import { BookOpen } from "lucide-react"; 
import { useNavigate } from 'react-router-dom';
import home from '../assets/home.png'


function HomePage() {
  const navigate = useNavigate();
  const handleGenerateStory = () => {
        navigate("/dashboard");
  };

  return (
    <>
      <div className='relative h-screen overflow-hidden'>
        <img
          className="absolute -mt-16 inset-0 -z-10 object-cover scale-x-[-1] opacity-40"
          src={home}
          alt="bg-image"
        />
        <div className='relative max-w-screen-2xl container mt-4 mx-auto h-full flex flex-col md:flex-row items-center justify-center md:px-20 px-5'>
          <div className='w-full md:w-1/2 space-y-6 '>
            <h1 className=' md:text-8xl text-5xl text-blue-600'>
              Welcome to
              <br />
              <span>the</span>
              <br />
              <p className='font-medium text-black'>AI <span className='typed-[Storyteller] typed-caret'></span></p>
            </h1>
            <p className='text-lg text-gray-700 mb-6'>
              Let your imagination run wild! Our AI storyteller brings your ideas to life by creating unique and fun stories just for you. Whether it’s an adventure, mystery, or fairy tale, the magic starts here!
            </p>
            <button
              onClick={handleGenerateStory}
              className="animate-pulse mx-auto bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full flex items-center"
            >
              <BookOpen className="mr-2" size={24} />
              Generate a Story
            </button>
          </div>
        </div>
      </div>
    </>

  )
}

export default HomePage