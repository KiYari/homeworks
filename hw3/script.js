
// 4.1 Треугольник
function triangle_ah() {
    let h = window.prompt("Введите длину высоту треугольника", "");
    let a = window.prompt("Введите длину стороны треугольника", "");

    if (h > 0 && a > 0) {
        window.alert("Ответ: Площадь треугольника - " + (a * h) / 2);
    } else {
        window.alert("Введены неверные данные.Попробуйте снова!");
    }
}

function triangle_aa() {
    let a1 = window.prompt("Введите длину 1-ой стороны треугольника", "");
    let a2 = window.prompt("Введите длину 2-ой стороны треугольника", "");
    let a = Number(window.prompt("Введите угол между сторонами треугольника. Угол должен быть больше 0," +
        " и меньше 180 градусов", ""));
    if (a1 > 0 && a2 > 0 && a > 0 && a < 180) {
        window.alert("Ответ: Площадь треугольника - " + (a1 * a2 * Math.sin(Math.PI * a / 180)) / 2);
    } else {
        window.alert("Введены неверные данные.Попробуйте снова!");
    }
}

//  4.2 Фибоначчи
function fibonacci() {
    let f1 = 1;
    let f2 = 1;
    let sum = 2;
    for (let i = 0; i < 8; i++) {
        let tmp = f2;
        f2 += f1;
        f1 = tmp;
        sum += f2;
    }
    window.alert("Ответ - " + sum);
}

// 4.3 Массивы

let matrice = new Array(4);
for (let i = 0; i < 4; i++) {
    matrice[i] = new Array(3);
      for (let j = 0; j < 3; j++) {
        matrice[i][j] = GetRandomInt(-10, 10);
    }
}

function print_mas(){
  for (let i = 0; i < 4; i++) {
    console.log(matrice[i]);
  }
}

function mas_change() {
  for (let i = 1; i < 4; i++) {
      for (let j = 0; j < 3; j++) {
          matrice[i][j] -= matrice[0][j];
    }
  }
  print_mas();
}

// 4.4 Функции

function GetRandomInt(max, min) {
    return Math.floor(min + Math.random() * (max + 1 - min));
}

function getArray(n){
  let array = new Array(n);
  for (let i = 0; i < n; i++) {
    array[i] = GetRandomInt(0, 10);
  }
  return array
}

function getResultArray(a, b) {
    return a.sort((a, b) => a - b)
}

//  Квадратная матрица

let table = document.querySelector('#table');
let arr = [9, 8, 7, 6, 5, 4, 3, 2, 1]; /* n = 3 */
arr = getResultArray(arr);
fillTable(table, arr);

function fillTable(table, arr) {
  let n = Math.sqrt(arr.length);
  let matrice2 = new Array(n);
  let ind = 0;

  for (let i = 0; i < n; i++) {
      matrice2[i] = new Array(n);
        for (let j = 0; j < n; j++) {
          matrice2[i][j] = 0;
      }
  }

  for (let j = 0; j < n; j++) {
    if (j % 2 == 0) {
        for (let i = n - 1; i >= 0; i--) {
          matrice2[i][j] = arr[ind];
          ind++;
        }
    } else {
        for (let i = 0; i < n; i++) {
          matrice2[i][j] = arr[ind];
          ind++;
        }
      }
    }
    for (let i = 0; i < n; i++) {
      let tr = document.createElement('tr');
      for (let j = 0; j < n; j++) {
        let td = document.createElement('td');
        td.innerHTML = matrice2[i][j];
        tr.appendChild(td);
        }
    table.appendChild(tr);
  }
}
