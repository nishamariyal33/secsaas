const express = require('express');
const router = express.Router();
const jobDeleteController = require('../controllers/jobDeleteController');

router.delete('/', jobDeleteController.handleDeleteJob);

module.exports = router;