-- Устройства конкретного человека
SELECT u.name,
    ut.type,
    dt.type,
    dt.name
FROM DeviceTypesToUserTypes dttut
    LEFT JOIN DeviceTypes dt ON dt.id = dttut.device_type_id
    LEFT JOIN UserTypes ut ON ut.id = dttut.user_type_id
    LEFT JOIN Users u ON u.user_type_id = ut.id
    AND u.name = 'Рогов Филимон Геннадиевич'
WHERE u.id IS NOT Null;
-- Самая большая зафиксированная температура
SELECT h.address,
    m.measure_time,
    m.value
FROM Measures m
    LEFT JOIN Devices d ON m.device_id = d.id
    LEFT JOIN DeviceTypes dt ON d.device_type_id = dt.id
    LEFT JOIN Houses h ON h.id = d.house_id
WHERE dt.type = 'thermostat'
ORDER BY m.value DESC
LIMIT 1;
-- Все "умные" дома. Дома в которых есть сценарии
SELECT DISTINCT h.*
FROM Houses h
    INNER JOIN Devices d ON h.id = d.house_id
    INNER JOIN ActivationsToDevices atd ON d.id = atd.device_id;