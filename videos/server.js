const app = require("./src/app");
const { DB_URI } = require("./src/config");
const mongoose = require("mongoose");
require('dotenv').config({ path: '../.env' });

mongoose.connect(DB_URI);

const port = process.env.PORT_VIDEOS || 3000;


app.listen(port, () => {
  console.log("running on port:" + port);
  console.log("--------------------------");
});
