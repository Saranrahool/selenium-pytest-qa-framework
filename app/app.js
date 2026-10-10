/*
 * Fleet Device Portal - a small demo web app used as the system under test.
 * It intentionally contains one known defect (see docs/bugs/BUG-001.md)
 * so the framework can demonstrate defect tracking with an expected-failure test.
 */
var Portal = (function () {
  var USERS = {
    tester: { password: "Passw0rd!", locked: false },
    locked_user: { password: "Passw0rd!", locked: true }
  };

  var DEVICES = [
    { id: "CAM-1001", bus: "Bus 101", type: "Forward camera", status: "Online", firmware: "4.2.1" },
    { id: "CAM-1002", bus: "Bus 101", type: "Stop-arm camera", status: "Online", firmware: "4.2.1" },
    { id: "NVR-2001", bus: "Bus 101", type: "Mobile recorder", status: "Online", firmware: "7.0.3" },
    { id: "CAM-1101", bus: "Bus 214", type: "Forward camera", status: "Offline", firmware: "4.1.9" },
    { id: "NVR-2101", bus: "Bus 214", type: "Mobile recorder", status: "Offline", firmware: "6.9.8" },
    { id: "CAM-1201", bus: "Bus 330", type: "Interior camera", status: "Online", firmware: "4.2.1" }
  ];

  var SESSION_KEY = "fdp_user";

  function login(username, password) {
    if (!username || !password) {
      return { ok: false, error: "Username and password are required." };
    }
    var user = USERS[username];
    if (!user || user.password !== password) {
      return { ok: false, error: "Invalid username or password." };
    }
    if (user.locked) {
      return { ok: false, error: "This account is locked. Contact your administrator." };
    }
    sessionStorage.setItem(SESSION_KEY, username);
    return { ok: true };
  }

  function logout() {
    sessionStorage.removeItem(SESSION_KEY);
  }

  function requireLogin() {
    if (!sessionStorage.getItem(SESSION_KEY)) {
      window.location.href = "index.html";
      return null;
    }
    return sessionStorage.getItem(SESSION_KEY);
  }

  function listDevices(statusFilter, searchText) {
    return DEVICES.filter(function (d) {
      var statusOk = !statusFilter || statusFilter === "All" || d.status === statusFilter;
      // BUG-001: search is case-sensitive, so "bus 214" does not match "Bus 214".
      var searchOk = !searchText || d.bus.indexOf(searchText) !== -1 || d.id.indexOf(searchText) !== -1;
      return statusOk && searchOk;
    });
  }

  function getDevice(id) {
    for (var i = 0; i < DEVICES.length; i++) {
      if (DEVICES[i].id === id) return DEVICES[i];
    }
    return null;
  }

  function isValidIPv4(value) {
    var parts = String(value).trim().split(".");
    if (parts.length !== 4) return false;
    return parts.every(function (p) {
      return /^\d{1,3}$/.test(p) && Number(p) >= 0 && Number(p) <= 255;
    });
  }

  function validateConfig(cfg) {
    var errors = {};
    if (!isValidIPv4(cfg.ip)) {
      errors.ip = "Enter a valid IPv4 address.";
    }
    var days = String(cfg.retention).trim();
    if (!/^\d+$/.test(days) || Number(days) < 1 || Number(days) > 90) {
      errors.retention = "Retention must be a whole number from 1 to 90 days.";
    }
    if (["720p", "1080p", "4K"].indexOf(cfg.resolution) === -1) {
      errors.resolution = "Select a supported resolution.";
    }
    return errors;
  }

  return {
    login: login,
    logout: logout,
    requireLogin: requireLogin,
    listDevices: listDevices,
    getDevice: getDevice,
    validateConfig: validateConfig
  };
})();
