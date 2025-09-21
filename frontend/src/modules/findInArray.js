export default function findInArray(arr, attr, val) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i][attr] === val) {
            return arr[i];
        }
    }

    return null;
}