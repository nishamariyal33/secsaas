const express = require('express');
const router = express.Router();
const jobListController = require('../controllers/jobListController');

router.get('/', jobListController.handleJobList);

module.exports = router;