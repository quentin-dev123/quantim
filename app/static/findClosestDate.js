function findClosestDate(dateStrings) {
    const targetDate = new Date(); // Target date is always now

    const parseDate = (dateString) => {
        return new Date(dateString);
    };


    if (!dateStrings || dateStrings.length === 0) {
        return null;
    }

    let closestDate = null;
    let minDifference = Infinity;

    for (const dateString of dateStrings) {
        const date = parseDate(dateString);
        if (isNaN(date)) {
            console.warn("Invalid date format:", dateString);
            continue;
        }
        const difference = Math.abs(targetDate - date);

        if (difference < minDifference) {
            minDifference = difference;
            closestDate = date;
        }
    }

    return closestDate;
}
