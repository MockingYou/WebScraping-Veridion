const csv = require("csv-parser");
const fs = require("fs");
const { Client } = require("@elastic/elasticsearch");
const config = require("config");
const elasticConfig = config.get("elastic");

const CSV_FILE_PATH = "../merged_data.csv";
const client = new Client({
	node: elasticConfig.cloudID,
	auth: {
		username: elasticConfig.username,
		password: elasticConfig.password,
	},
	apiKey: elasticConfig.apiKey,
});

async function indexData() {
	let data = [];

	fs.createReadStream(CSV_FILE_PATH)
		.pipe(csv())
		.on("data", (row) => {
			data.push(row);
		})
		.on("end", async () => {
			for (let i = 0; i < data.length; i++) {
				const { domain } = data[i];
				const id = domain;
				await client
					.index({
						index: "search_index",
						id: id,
						body: data[i],
						op_type: "create",
					})
					.catch((error) => {
						if (error.statusCode === 409) {
							console.error(
								`Document with ID '${id}' already exists.`,
							);
						} else {
							console.error("Error indexing document:", error);
						}
					});
			}
			console.log("Data indexed successfully.");
		});
}
async function searchData(body) {
  const shouldClauses = [];
  if (body.domain) {
    shouldClauses.push({ regexp: { domain: `.*${body.domain.toLowerCase()}.*` } });
  }
  if (body.company_commercial_name) {
    shouldClauses.push({ regexp: { company_commercial_name: `.*${body.company_commercial_name.toLowerCase()}.*` } });
  }
  if (body.company_legal_name) {
    shouldClauses.push({ regexp: { company_legal_name: `.*${body.company_legal_name.toLowerCase()}.*` } });
  }
  if (body.company_all_available_names) {
    shouldClauses.push({ regexp: { company_all_available_names: `.*${body.company_all_available_names.toLowerCase()}.*`  } });
  }
  if (body.phone_number) {
    shouldClauses.push({ match: { phone_number: `.*${body.phone_number.toString()}.*` } });
  }
  if (body.social) {
    shouldClauses.push({ regexp: { social: `.*${body.social.toLowerCase()}.*` } });
  }
  if (body.location) {
    shouldClauses.push({ regexp: { location: `.*${body.location.toLowerCase()}.*` } });
  }
  try {
    const response = await client.search({
      index: "search_index",
      query: {
        bool: {
          should: shouldClauses
        }
      },
    });
    let responseMap = response.hits.hits.map(hit => hit._source);
    return responseMap[0]
  } catch (error) { 
    return error
  }
}

module.exports = { searchData, indexData }