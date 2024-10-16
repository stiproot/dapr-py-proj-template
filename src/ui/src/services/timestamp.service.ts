const moment = require("moment");

export const now = () => moment().utc().format();

export const toLocale = (timestamp: string): string => moment.utc(timestamp).local().format('DD/MM/YYYY');