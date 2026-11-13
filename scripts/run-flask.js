const { spawn } = require("child_process");
const path = require("path");

const root = path.join(__dirname, "..");
const appPath = path.join(root, "backend", "app.py");
const candidates =
  process.platform === "win32" ? ["python", "py", "python3"] : ["python3", "python"];

function run(command) {
  const child = spawn(command, [appPath], {
    cwd: root,
    stdio: "inherit",
    shell: process.platform === "win32",
  });

  child.on("error", (error) => {
    if (error.code === "ENOENT") {
      tryNext(command);
      return;
    }
    console.error(error);
    process.exit(1);
  });

  child.on("exit", (code, signal) => {
    if (signal) {
      process.kill(process.pid, signal);
      return;
    }
    process.exit(code ?? 0);
  });
}

let index = 0;
function tryNext(failedCommand) {
  index += 1;
  if (index >= candidates.length) {
    console.error(
      `Could not start Flask. Install Python 3 and make sure it is on your PATH (tried ${failedCommand}).`
    );
    process.exit(1);
  }
  run(candidates[index]);
}

run(candidates[0]);
