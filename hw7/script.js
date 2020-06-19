//interface
var dir, start_pause, restart, change_player, section;
var game, info;
var x_fault, y_fault;
//logic
var bGame;
//main field
var canvas, ctx;
//field background
var image = new Image(900, 600); //фон
image.src = 'bg.jpg'; //фон
//data
var name = ""; //имя игрока
var score; //счёт
var hp; //здоровья
var spec; //ульта
var level = 1;
var enemy_list = []; //враги
var bullet_list = []; //ядра
//obj
var gun; //пушка
var gun_x, gun_y; //координаты пушки
var angle; //начальный угол орудия
var draw_angle;
var tic;
//sprites
var en1 = new Image(200, 200);
en1.src = 'enemy1.png';
var en2 = new Image(150, 150);
en2.src = 'enemy2.png';
var en3 = new Image(150, 150);
en3.src = 'enemy3.png';
var en4 = new Image(150, 150);
en4.src = 'enemy4.png';
//timers
var game_timer;


function new_session() {
    check_name();
    init();
}

function init() {
    dir = "game";
    canvas = document.getElementById('canvas');
    gun = new Gun;
    gun_x = 50;
    gun_y = canvas.height - 50;
    score = 0;
    hp = 5;
    spec = 3;
    level = 1;
    angle = toRad(45);
    draw_angle = toRad(45);
    tic = 0;
    enemy_list = [];
    bullet_list = [];
    if (canvas.getContext) {
        ctx = canvas.getContext('2d');
        drawBack(ctx, canvas.width, canvas.height);
        x_fault = canvas.getBoundingClientRect().left;
        y_fault = canvas.getBoundingClientRect().top;
    }
    start_pause = document.getElementById("btn1");
    restart = document.getElementById("btn2");
    change_player = document.getElementById("btn3");
    section = document.getElementById("btn4");
    game = document.getElementById("game");
    info = document.getElementById("info");
    bGame = false;
}

function drawBack(ctx, w, h) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(image, 0, 0);
    draw_info();
    for (i = 0; i < bullet_list.length; i++)
        bullet_list[i].draw(ctx);
    for (i = 0; i < enemy_list.length; i++)
        enemy_list[i].draw(ctx);
    gun.draw(ctx);
}

function toDeg(num) { //Радианы -> градусы
    return num * 180 / Math.PI;
}

function toRad(num) { //Градусы -> радианы
    return num * Math.PI / 180;
}

function shoot() {
    if (bGame && tic >= 150) {
        tic = 0;
        bullet_list.push(new Bullet(angle));
    }
}

function ult() {
    if (score >= 500) {
        score -= 500;
        enemy_list = [];
        bullet_list = [];
    }
}

function rotate(event) {
    if (bGame) {
        let dx = event.x - x_fault - gun_x;
        let dy = canvas.height + y_fault - event.y - 50;
        if (dy >= 0 && dx >= 0) {
            angle = Math.atan2(dy, dx);
            draw_angle = Math.atan2(dx, dy);
        }
    }
}

function change_status() {
    if (!bGame) {
        bGame = true;
        start_pause.value = "Pause";
        restart.disabled = true;
        change_player.disabled = true;
        section.disabled = true;
        game_timer = setInterval('play();', 1);
        return;
    }
    if (bGame) {
        bGame = false;
        start_pause.value = "Play";
        restart.disabled = false;
        change_player.disabled = false;
        section.disabled = false;
        clearInterval(game_timer);
        return;
    }
}

function change_section() {
    if (dir == "info") {
        dir = "game";
        start_pause.disabled = false;
        restart.disabled = false;
        change_player.disabled = false;
        section.value = "Rules&Records";
        info.style.display = "none";
        game.style.display = "block";
        return;
    }
    if (dir == "game") {
        dir = "info";
        start_pause.disabled = true;
        restart.disabled = true;
        change_player.disabled = true;
        section.value = "Game";
        info.style.display = "block";
        game.style.display = "none";
        display_table();
        return;
    }
}

function randomInt(min, max) {
    return min + Math.floor(Math.random() * (max - min));
}

function play() {
    if (hp > 0) {
        let step = 0;
        drawBack(ctx, canvas.width, canvas.height);
        tic++;
        level = score / 500 + 1;
        en_amount = 3 + level * 2;

        for (i = 0; i < bullet_list.length; i++) {
            if (bullet_list[i].posX + bullet_list[i].size >= canvas.width)
                bullet_list.splice(i--, 1);
        }

        for (i = 0; i < bullet_list.length; i++) {
            for (j = 0; j < enemy_list.length; j++) {
                if (clash(bullet_list[i], enemy_list[j])) {
                    score += enemy_list[j].points;
                    enemy_list.splice(j--, 1);
                }
            }
        }

        for (j = 0; j < enemy_list.length; j++) {
            if (enemy_list[j].posX <= 0) {
                enemy_list.splice(j--, 1);
                hp--;
            }
        }

        for (j = 0; j < enemy_list.length; j++) {
            enemy_list[j].posX -= enemy_list[j].speed;
        }


        while (enemy_list.length < en_amount)
            get_enemy(step);
            step += 150;
    } else {
        end_game();
    }
}

//Gun
Gun = new Class({
    draw: function(ctx) {
        with(this) {
            //first
            ctx.save()
            ctx.translate(gun_x, gun_y);
            ctx.rotate(draw_angle);
            ctx.fillStyle = '#FFC0CB';
            ctx.beginPath();
            ctx.arc(0, 0, 35, 2 * Math.PI, Math.PI, false);
            ctx.moveTo(15 - 50, 0);
            ctx.lineTo(30 - 50, 0 - 65);
            ctx.lineTo(70 - 50, 0 - 65);
            ctx.lineTo(85 - 50, 0);
            ctx.lineTo(15 - 50, 0);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
            //second
            ctx.save()
            if (tic >= 100)
                ctx.fillStyle = 'green';
            else
                ctx.fillStyle = 'red';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);
            ctx.lineTo(20, canvas.height - 30);
            ctx.lineTo(80, canvas.height - 30);
            ctx.lineTo(100, canvas.height);
            ctx.lineTo(0, canvas.height);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }
    }
})

Bullet = new Class({
    initialize: function(angle) {
        this.posX = 0;
        this.posY = 0;
        this.speed = 50;
        this.size = 5;
        this.angle = angle;
    },
    fly: function() {
        p1 = this.posX * Math.tan(this.angle);
        p2 = 0.2 * (this.posX ** 2);
        p3 = 2 * (this.speed ** 2) * (Math.cos(this.angle) ** 10);
        this.posY = p1 - (p2 / p3);
        this.posX += this.speed * Math.cos(this.angle) / 2;
    },
    draw: function(ctx) {
        ctx.fillStyle = '#000000';
        ctx.save();
        ctx.translate(gun_x, gun_y);
        ctx.beginPath();
        ctx.arc(this.posX, -this.posY, this.size + 10, 0, 2 * Math.PI, false);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
        this.fly();
    }
})

//Enemies
enemy_data = [{
    size: 200,
    speed: 2 * level / 5,
    points: 5,
    img: en1
}, {
    size: 150,
    speed: (2 * level + 2) / 5,
    points: 10,
    img: en2
}, {
    size: 150,
    speed: (2 * level + 3) / 5,
    points: 20,
    img: en3
}, {
    size: 150,
    speed: (2 * level + 4) / 5,
    points: 40,
    img: en4
}]

Enemy = new Class({
    initialize: function(pX, pY, sz, sp, pts, im) {
        this.posX = pX; // позиция фигуры по X
        this.posY = pY; // позиция фигуры по Y
        this.size = sz;
        this.speed = sp;
        this.points = pts;
        this.img = im;
    },
    draw: function(ctx) {
        ctx.drawImage(this.img, this.posX - this.size / 2, canvas.height - this.posY - this.size / 2, this.size, this.size);
    },
})

function get_enemy() {
    type = randomInt(0, 4);
    x = canvas.width + randomInt(100, 1000);
    y = randomInt(100, canvas.height - 100);
    data = enemy_data[type];
    enemy_list.push(new Enemy(x, y, data.size, data.speed, data.points, data.img));
}

//info
function draw_info() {
    ctx.fillStyle = "#fd00ff";
    ctx.font = "30px Arial";
    ctx.fillText(get_hp(), 10, 40);
    ctx.font = "30px Arial";
    ctx.fillText(score, 15, 70);
}
//hp str
function get_hp() {
    str = '';
    i = 0;
    while (i++ < hp) str += '❤';
    while (i++ <= 5) str += '♡';
    return str;
}
//name
function check_name() {
    firstName = prompt('Как Вас зовут?');
    if (Boolean(firstName)) {
        name = firstName;
        alert("Приятной игры, " + firstName)
    } else
        check_name();
}

function clash(figure1, figure2) {
    clashX = false;
    clashY = false;
    if (figure1.posX - figure2.size / 2 <= figure2.posX && figure1.posX + figure2.size / 2 >= figure2.posX) clashX = true;
    if (figure1.posY - figure2.size / 2 <= figure2.posY && figure1.posY + figure2.size / 2 >= figure2.posY) clashY = true;
    return clashX && clashY;
}

function end_game() {
    alert("GAME OVER");
    localStorage.setItem(name, score);
    change_status();
    change_section();
}

function display_table() {
    let html = "<table id=\"gen\"><th>ИМЯ</th><th>ОЧКИ</th>";
    for (let i = 0; i < localStorage.length && i < 15; i++) {
        html += "<tr aling=\"center\">";
        for (let j = 0; j < 1; j++) {
            let key = localStorage.key(i)
            html += "<td>" + localStorage.key(i) + "</td>";
            html += "<td>" + localStorage.getItem(key) + "</td>"
        }
        html += "</tr>";
    }
    html += "</table>";

    document.getElementById("top").innerHTML = html;
}