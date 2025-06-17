const fs = require("fs");
const path = require("path");

const DATA_PATH = path.resolve(__dirname, "../data/visits.json");

exports.handler = async function (event) {
  const params = new URLSearchParams(event.rawUrl.split("?")[1]);
  const site = params.get("site");

  if (!site) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "Missing 'site' query parameter" }),
    };
  }

  try {
    let visitsData = {};
    if (fs.existsSync(DATA_PATH)) {
      visitsData = JSON.parse(fs.readFileSync(DATA_PATH));
    }

    if (!visitsData[site]) {
      visitsData[site] = 0;
    }

    visitsData[site] += 1;

    fs.writeFileSync(DATA_PATH, JSON.stringify(visitsData, null, 2));

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({ site, count: visitsData[site] }),
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message }),
    };
  }
};