const jalaliInput = document.getElementById("jalali_date");
const picker = document.getElementById("datepicker");
const hiddenInput = document.getElementById("gregorian_date");

let currentYear = 1404;
let currentMonth = 1;

// تعداد روزهای هر ماه شمسی
function getMonthDays(month, year) {
    if (month <= 6) return 31;
    if (month <= 11) return 30;
    return isLeapJalali(year) ? 30 : 29;
}

// تشخیص سال کبیسه شمسی
function isLeapJalali(jy) {
    return (((jy + 38) * 31) % 128) < 31;
}

// تبدیل شمسی به میلادی (دقیق)
function jalaliToGregorian(jy, jm, jd) {
    let gy;
    if (jy > 979) {
        gy = 1600;
        jy -= 979;
    } else {
        gy = 621;
    }

    let days =
        (365 * jy) +
        Math.floor(jy / 33) * 8 +
        Math.floor(((jy % 33) + 3) / 4);

    for (let i = 1; i < jm; ++i) {
        days += getMonthDays(i, jy);
    }

    days += jd - 1;
    gy += 400 * Math.floor(days / 146097);
    days %= 146097;

    if (days > 36524) {
        gy += 100 * Math.floor(--days / 36524);
        days %= 36524;
        if (days >= 365) days++;
    }

    gy += 4 * Math.floor(days / 1461);
    days %= 1461;

    if (days > 365) {
        gy += Math.floor((days - 1) / 365);
        days = (days - 1) % 365;
    }

    let gd = days + 1;
    const sal_a = [
        0, 31,
        (gy % 4 === 0 && gy % 100 !== 0) || gy % 400 === 0 ? 29 : 28,
        31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    ];

    let gm;
    for (gm = 1; gm <= 12; gm++) {
        if (gd <= sal_a[gm]) break;
        gd -= sal_a[gm];
    }

    return [gy, gm, gd];
}

// ساخت DatePicker
function renderPicker() {
    picker.innerHTML = "";

    const header = document.createElement("div");
    header.style.marginBottom = "10px";
    header.style.textAlign = "center";

    const prev = document.createElement("button");
    prev.innerText = "◀";
    prev.onclick = () => {
        if (currentMonth === 1) {
            currentMonth = 12;
            currentYear--;
        } else {
            currentMonth--;
        }
        renderPicker();
    };

    const next = document.createElement("button");
    next.innerText = "▶";
    next.onclick = () => {
        if (currentMonth === 12) {
            currentMonth = 1;
            currentYear++;
        } else {
            currentMonth++;
        }
        renderPicker();
    };

    const title = document.createElement("span");
    title.innerText = ` ${currentYear} / ${currentMonth} `;
    title.style.margin = "0 10px";

    header.appendChild(prev);
    header.appendChild(title);
    header.appendChild(next);
    picker.appendChild(header);

    const days = getMonthDays(currentMonth, currentYear);

    for (let d = 1; d <= days; d++) {
        const day = document.createElement("div");
        day.className = "day";
        day.innerText = d;

        day.onclick = () => {
            jalaliInput.value = `${currentYear}/${String(currentMonth).padStart(2, '0')}/${String(d).padStart(2, '0')}`;

            const g = jalaliToGregorian(currentYear, currentMonth, d);
            hiddenInput.value = `${g[0]}-${String(g[1]).padStart(2, '0')}-${String(g[2]).padStart(2, '0')}`;

            picker.style.display = "none";
        };

        picker.appendChild(day);
    }
}

// باز و بسته شدن
jalaliInput.onclick = () => {
    picker.style.display = "block";
    renderPicker();
};

// بستن با کلیک بیرون
document.addEventListener("click", (e) => {
    if (!picker.contains(e.target) && e.target !== jalaliInput) {
        picker.style.display = "none";
    }
});
