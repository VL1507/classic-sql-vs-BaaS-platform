Parse.Cloud.define("findUserDeviceTypes", async (request) => {
    // Устройства конкретного человека
    const userName = request.params.name;

    if (!userName) {
        return { results: [], message: "Не передан параметр name" }
    }

    const userQuery = new Parse.Query("Users");
    userQuery.equalTo("name", userName);
    userQuery.include("user_type_id");

    let user;
    try {
        user = await userQuery.first({ useMasterKey: true });
    } catch (e) {
        console.error("Ошибка при поиске пользователя:", e.message);
        throw e;
    }

    if (!user) {
        return { results: [], message: "Пользователь не найден" };
    }

    const userType = user.get("user_type_id");

    if (!userType) {
        return { results: [], message: "У пользователя нет типа" };
    }

    const linkQuery = new Parse.Query("DeviceTypesToUserTypes");
    linkQuery.equalTo("user_type_id", userType);
    linkQuery.include(["user_type_id", "device_type_id"]);
    linkQuery.include("device_type_id.type");
    linkQuery.include("device_type_id.name");

    let links;
    try {
        links = await linkQuery.find({ useMasterKey: true });
    } catch (e) {
        console.error("Ошибка при поиске связей:", e.message);
        throw e;
    }

    const result = links.map(link => {
        const ut = link.get("user_type_id");
        const dt = link.get("device_type_id");
        return {
            userName: user.get("name"),
            userType: ut ? ut.get("type") : null,
            deviceType: dt ? dt.get("type") : null,
            deviceName: dt ? dt.get("name") : null
        };
    });

    return result;
});

Parse.Cloud.define("getHousesWithActivatedDevices", async (request) => {
    // Все "умные" дома. Дома в которых есть сценарии
    const useMaster = { useMasterKey: true };

    const ActivationToDevice = Parse.Object.extend("ActivationsToDevices");
    const atdQuery = new Parse.Query(ActivationToDevice);
    atdQuery.include("device_id");

    const activations = await atdQuery.find(useMaster);

    if (activations.length === 0) {
        return { houses: [], count: 0, message: "No activations found" };
    }

    const deviceIds = new Set();
    activations.forEach(atd => {
        const device = atd.get("device_id");
        if (device && device.id) {
            deviceIds.add(device.id);
        }
    });

    if (deviceIds.size === 0) {
        return { houses: [], count: 0, message: "No devices in activations" };
    }

    const Device = Parse.Object.extend("Devices");
    const deviceQuery = new Parse.Query(Device);
    deviceQuery.containedIn("objectId", Array.from(deviceIds));
    deviceQuery.include("house_id");

    const devices = await deviceQuery.find(useMaster);

    const houseMap = new Map();

    devices.forEach(device => {
        const house = device.get("house_id");
        if (house && house.id) {
            houseMap.set(house.id, house);
        }
    });

    const uniqueHouses = Array.from(houseMap.values());

    const result = uniqueHouses.map(house => {
        return {
            objectId: house.id,
            address: house.get("address") || null
        };
    });

    return { houses: result };

});



Parse.Cloud.define("getMaxThermostatValue", async (request) => {
    // Самая большая зафиксированная температура
    const DeviceType = Parse.Object.extend("DeviceTypes");
    const dtQuery = new Parse.Query(DeviceType);
    dtQuery.equalTo("type", "thermostat");

    const thermostatType = await dtQuery.first({ useMasterKey: true });

    if (!thermostatType) {
        throw new Parse.Error(Parse.Error.OBJECT_NOT_FOUND, "Thermostat device type not found");
    }

    const Device = Parse.Object.extend("Devices");
    const deviceQuery = new Parse.Query(Device);
    deviceQuery.equalTo("device_type_id", thermostatType);

    const devices = await deviceQuery.find({ useMasterKey: true });

    if (devices.length === 0) {
        return { message: "No thermostat devices found" };
    }

    const Measure = Parse.Object.extend("Measures");

    const measureQuery = new Parse.Query(Measure);
    measureQuery.containedIn("device_id", devices);
    measureQuery.descending("value");
    measureQuery.limit(1);

    measureQuery.include(["device_id.house_id", "device_id"]);

    const topMeasure = await measureQuery.first({ useMasterKey: true });

    if (!topMeasure) {
        return { message: "No measurements found for thermostats" };
    }

    const device = topMeasure.get("device_id");
    const house = device?.get("house_id");

    const result = {
        address: house ? house.get("address") : null,
        measure_time: topMeasure.get("measure_time"),
        value: topMeasure.get("value")
    };

    return result;
});

Parse.Cloud.define("ping", async (request) => {
    // Проверка работы сервера
    return { status: "alive", receivedParams: request.params };
});