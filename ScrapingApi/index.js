const express = require("express");
const cors = require("cors");
const { searchData, indexData } = require('./utils/elasticsearch')
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

app.post("/api/search", async (req, res) => {
	try {
		const body = req.body;
		const results = await searchData(body);
		res.json(results);
	} catch (error) {
		console.error("Error searching data:", error);
		res.status(500).json({ error: "Internal server error" });
	}
});

app.listen(port, async () => {
	console.log(`Example app listening on port ${port}`);
	await indexData();
});
