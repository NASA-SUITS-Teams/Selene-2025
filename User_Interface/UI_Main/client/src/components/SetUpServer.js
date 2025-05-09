const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'client/build')));

const activeConnections = { TSS: null };

app.post('/api/connect', (req, res) => {
  const { system, ipAddress } = req.body;
  
  if (system !== 'TSS') {
    return res.status(400).json({ error: 'Only TSS connections are supported' });
  }

  if (activeConnections.TSS && !activeConnections.TSS.killed) {
    activeConnections.TSS.kill();
    activeConnections.TSS = null;
  }

  try {
    const scriptPath = path.join(__dirname, 'scripts', 'tss_connector.py');
    const pythonProcess = spawn('python', [scriptPath, ipAddress]);

    activeConnections.TSS = pythonProcess;

    pythonProcess.stdout.on('data', (data) => {
      console.log(`TSS output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`TSS error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      console.log(`TSS process exited with code ${code}`);
      activeConnections.TSS = null;
    });

    res.status(200).json({ 
      success: true, 
      message: `TSS connection initiated at ${ipAddress}` 
    });
  } catch (error) {
    console.error('TSS connection error:', error);
    res.status(500).json({ 
      error: `TSS connection failed: ${error.message}` 
    });
  }
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});