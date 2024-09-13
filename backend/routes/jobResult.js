const express = require('express');
const router = express.Router();
const jobResultController = require('../controllers/jobResultController.js');

router.post('/', jobResultController.handleJobResult);

module.exports = router;