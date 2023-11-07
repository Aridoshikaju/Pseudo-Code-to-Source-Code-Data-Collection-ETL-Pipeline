import express from "express";
import fetch from "node-fetch";

const app = express();
const port = 8080;

app.get("/getFile", async (req, res) => {
  const repoOwner = req.query.repoOwner;
  const repoName = req.query.repoName;
  const filePath = req.query.filePath;
  const accessToken = req.query.accessToken;

  if (!repoOwner || !repoName || !filePath) {
    res.status(400).json({ error: "Missing parameters: owner, repo, or path" });
    return;
  }

  const apiUrl = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/7.8/${filePath}`;
  const headers = new fetch.Headers();

  if (accessToken) {
    headers.append("Authorization", `Bearer ${accessToken}`);
  }

  try {
    const response = await fetch(apiUrl, { method: "GET", headers });

    if (response.ok) {
      const fileContent = await response.text();
      res.json({ content: fileContent });
    } else {
      res.status(response.status).json({ error: "GitHub API request failed" });
    }
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
