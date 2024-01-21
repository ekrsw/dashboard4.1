from datetime import datetime

def datetime_to_serial(dt, base_date=datetime(1899, 12, 30)):
    """
    datetimeオブジェクトをシリアル値に変換する。

    :param dt: 変換するdatetimeオブジェクト
    :param base_date: シリアル値の基準日（デフォルトは1899年12月30日）
    :return: シリアル値
    """
    dt = datetime(dt.year, dt.month, dt.day)
    return (dt - base_date).total_seconds() / (24 * 60 * 60)

def serial_to_datetime(serial, base_date=datetime(1899, 12, 30)):
    """
    シリアル値をdatetimeオブジェクトに変換する。

    :param serial: 変換するシリアル値
    :param base_date: シリアル値の基準日（デフォルトは1899年12月30日）
    :return: datetimeオブジェクト
    """
    dt = datetime(dt.year, dt.month, dt.day)
    return base_date + dt.timedelta(days=serial)

def current_time_to_serial(base_date=datetime(1899, 12, 30)):
    """
    現在日時をシリアル値に変換する。

    :return: シリアル値
    """
    current_time = datetime.now()
    serial_value = (current_time - base_date).total_seconds() / (24 * 60 * 60)
    return serial_value