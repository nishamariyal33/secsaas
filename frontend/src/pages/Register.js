import { useState, useEffect, useContext } from 'react';
import { baseUrl } from '../shared';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginContext } from '../App';
import axios from 'axios';

export default function Register() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [name, setName] = useState();
    const [address, setAddress] = useState();
    const [email, setEmail] = useState();
    const [adDomainUrl, setadDomainUrl] = useState();
    const [basedn, setBasedn] = useState();

    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        localStorage.clear();
        setLoggedIn(false);
    }, []);

   async function login(e) {
        e.preventDefault();
        const response = await axios.post(
            "http://localhost:4000/register", 
            {
                name, email, adDomainUrl, address, 'basedn':"DN"
            },
        );
        const data=response.data;
                console.log("qqqqq ",data);
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                // setLoggedIn(true);
                navigate(
                    location?.state?.previousUrl
                        ? location.state.previousUrl
                        : `/login/tenantId=${data}`
                );
            
    }

    return (
        <form className="m-2 w-full max-w-sm" id="customer" onSubmit={login}>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label for="email">Email</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                        }}
                    />
                </div>
            </div>
            
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label for="name">Name</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="name"
                        type="text"
                        value={name}
                        onChange={(e) => {
                            setName(e.target.value);
                        }}
                    />
                </div>
            </div>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label for="address">Address</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="address"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="address"
                        value={address}
                        onChange={(e) => {
                            setAddress(e.target.value);
                        }}
                    />
                </div>
            </div>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label for="adDomainUrl">Active Directory Domain URL</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="adDomainUrl"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="adDomainUrl"
                        value={adDomainUrl}
                        onChange={(e) => {
                            setadDomainUrl(e.target.value);
                        }}
                    />
                </div>
            </div>

            {/* <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label for="basedn">Base Distinguished Name</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="basedn"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="basedn"
                        value={basedn}
                        onChange={(e) => {
                            setBasedn(e.target.value);
                        }}
                    />
                </div>
            </div> */}

            <button className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">
                Register
            </button>
        </form>
    );
}
