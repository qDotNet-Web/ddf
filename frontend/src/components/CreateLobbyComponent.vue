<template>
    <div class="container my-auto vertical-center dff-padding-top" id="app">
        <img src="@/assets/logo.png" alt="Logo" class="icon mb-4">
        <h1 class="dff-h1 mb-4">Der Dümmste fliegt!</h1>

        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <label class="input-group-text" for="ip_roundLength">Rundenlänge (min)</label>
            </div>
            <select class="custom-select" id="ip_roundLength">
                <option value="1">1</option>
                <option value="2">2</option>
                <option selected value="3">3</option>
            </select>
        </div>

        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <label class="input-group-text" for="ip_playercount">Spieleranzahl</label>
            </div>
            <select class="custom-select" id="ip_playerCount">
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option selected value="10">10</option>
            </select>
        </div>

        <div class="input-group mb-3">
            <div class="input-group-prepend">
                <label class="input-group-text" for="ip_maxPlayerLives">Max. Spielerleben</label>
            </div>
            <select class="custom-select" id="ip_playercount">
                <option value="1">1</option>
                <option value="2">2</option>
                <option selected value="3">3</option>
            </select>
        </div>
    </div>
    
</template>