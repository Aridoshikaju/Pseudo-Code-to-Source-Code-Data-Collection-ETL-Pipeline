//File download code

// import express from "express";
// import express from "express";
// import fetch from "node-fetch";
// import archiver from "archiver";

// const app = express();
// const port = 8080;

// app.get("/getFile", async (req, res) => {
//   const repoOwner = "guzzle"; // Replace with your GitHub username
//   const repoName = "guzzle"; // Replace with your GitHub repository name
//   const filePath = "docs/conf.py"; // Replace with the file path you want to access
//   const accessToken = "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"; // Replace with your GitHub access token (if needed)

//   // const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${filePath}`;

//   const apiUrl = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/7.8/${filePath}`;
//   const headers = new fetch.Headers();

//   if (accessToken) {
//     headers.append("Authorization", `Bearer ${accessToken}`);
//   }

//   try {
//     const response = await fetch(apiUrl, { method: "GET", headers });

//     //     if (response.ok) {
//     //       const data = await response.json();

//     //       if (data.content) {
//     //         const fileContent = Buffer.from(data.content, "base64").toString(
//     //           "utf-8"
//     //         );
//     //         res.send(fileContent);
//     //       } else {
//     //         res.status(404).send("File not found");
//     //       }
//     //     } else {
//     //       res.status(response.status).send("GitHub API request failed");
//     //     }
//     //   } catch (error) {
//     //     console.error("Error:", error);
//     //     res.status(500).send("Internal server error");
//     //   }
//     // });
//     //     if (response.ok) {
//     //       const fileContent = await response.text();
//     //       res.send(fileContent);
//     //     } else {
//     //       res.status(response.status).send("GitHub API request failed");
//     //     }
//     //   } catch (error) {
//     //     console.error("Error:", error);
//     //     res.status(500).send("Internal server error");
//     //   }
//     // });

//     if (response.ok) {
//       const fileContent = await response.text();

//       // Create a zip archive
//       const archive = archiver("zip");
//       archive.append(fileContent, { name: filePath });

//       // Pipe the archive to the response
//       res.attachment("file.zip"); // Set the response to download the zip file
//       archive.pipe(res);
//       archive.finalize();
//     } else {
//       res.status(response.status).send("GitHub API request failed");
//     }
//   } catch (error) {
//     console.error("Error:", error);
//     res.status(500).send("Internal server error");
//   }
// });
// app.get("/", (req, res) => {
//   res.send("Hello world");
// });
// app.listen(port, () => {
//   console.log(`Server is running on port ${port}`);
// });

// only contents directly

import express from "express";
import fetch from "node-fetch";

const app = express();
const port = 8080;

app.get("/getFile", async (req, res) => {
  const repoOwner = "guzzle"; // GitHub username provided as a query parameter
  const repoName = "guzzle"; // GitHub repository name provided as a query parameter
  const filePath = "docs/conf.py"; // File path you want to access provided as a query parameter
  const accessToken = "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"; // Replace with your GitHub access token (if needed)

  if (!repoOwner || !repoName || !filePath) {
    res.status(400).send("Missing parameters: owner, repo, or path");
    return;
  }

  const apiUrl = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/7.8/${filePath}`; // Assuming the main branch
  const headers = new fetch.Headers();

  if (accessToken) {
    headers.append("Authorization", `Bearer ${accessToken}`);
  }

  try {
    const response = await fetch(apiUrl, { method: "GET", headers });

    if (response.ok) {
      const fileContent = await response.text();
      res.setHeader("Content-Type", "text/plain");
      // res.send("<pre>" + fileContent + "</pre>");
      res.send(fileContent);
    } else {
      res.status(response.status).send("GitHub API request failed");
    }
  } catch (error) {
    console.error("Error:", error);
    res.status(500).send("Internal server error");
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
