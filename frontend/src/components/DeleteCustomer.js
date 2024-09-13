import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';

export default function DeleteCustomer(props) {
    const [show, setShow] = useState(props.show);
    const jobId=props.jobId;
    console.log("xxxxxx ",jobId)
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <button
                onClick={props.toggleShow}
                className="block m-2 bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
            >
                Delete
            </button>

            <Modal
                show={props.show}
                onHide={handleClose}
                backdrop="static"
                keyboard={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to delete this job?</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            props.deleteScan(jobId);
                        }}
                        id="editmodal"
                        className="w-full max-w-sm"
                    >
                        {/* <div className="md:flex md:items-center mb-6">
                            <div className="md:w-1/3">
                                <label
                                    className="block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4"
                                    for="targetUrl"
                                >
                                    Target URL
                                </label>
                            </div>
                            <div className="md:w-2/3">
                                <input
                                    className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                                    id="targetUrl"
                                    placeholder="192.168.56.101"
                                    type="text"
                                    value={targetUrl}
                                    onChange={(e) => {
                                        setTargetUrl(e.target.value);
                                    }}
                                />
                            </div>
                        </div>
                        <div className="md:flex md:items-center mb-6">
                            <div className="md:w-1/3">
                                <label
                                    className="block text-gray-500 font-bold md:text-right mb-1 md:mb-0 pr-4"
                                    for="scanType"
                                >
                                    Scan Type
                                </label>
                            </div>
                            <div className="md:w-2/3">
                                <input
                                    className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                                    id="scanType"
                                    placeholder="hostedscan"
                                    type="text"
                                    value={scanType}
                                    onChange={(e) => {
                                        setScanType(e.target.value);
                                    }}
                                />
                            </div>
                        </div> */}
                    </form>
                </Modal.Body>
                <Modal.Footer>
                    <button
                        className="bg-slate-400 hover:bg-slate-500 text-white font-bold py-2 px-4 rounded"
                        onClick={props.toggleShow}
                    >
                        No
                    </button>
                    <button
                        className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
                        form="editmodal"
                    >
                        Yes
                    </button>
                </Modal.Footer>
            </Modal>
        </>
    );
}
