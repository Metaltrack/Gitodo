export const log_level = Object.freeze({
    INFO: "INFO",
    ERROR: "ERROR",
    WARNING: "WARNING",
    CRITICAL: "CRITICAL"
})

export function log(level, file, msg) {
    var timestamp = new Date().toISOString();

    console.log(JSON.stringify({
        "Level": level,
        "Time-Stamp": timestamp,
        "From-File": file,
        "Message": msg
    }));
    return;
}
