const express = require('express');
const router = express.Router();
const jobController = require('../controllers/jobController');

router.post('/', jobController.handleNewJob);

module.exports = router;