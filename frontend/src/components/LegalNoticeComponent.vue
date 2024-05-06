<style scoped>
*{
    user-select: none;
}
</style>

<template>
    <div class="container my-auto" id="app">
        <div class="container mb-4 center" @click="goHome">
            <img src="@/assets/logo.png" alt="Logo" class="icon mb-4">
            <h1 class="dff-h1">Der Dümmste fliegt!</h1>
        </div>
        <div class="impressum center">
            <h1>Impressum</h1>
            <h2 id="m46">Diensteanbieter</h2>
            Marvin Brückner
            Florian-Geyer-Siedlung 18
            07907 Oettersdorf
            Deutschland

            <h2 id="m56">Kontaktmöglichkeiten</h2>E-Mail-Adresse: <a href="mailto:marvin@qdotnet.de">marvin@qdotnet.de</a>
            Telefon: 016096208386

            <p class="seal"><a href="https://datenschutz-generator.de/" title="Rechtstext von Dr. Schwenke - für weitere Informationen bitte anklicken." target="_blank" rel="noopener noreferrer nofollow">Erstellt mit kostenlosem Datenschutz-Generator.de von Dr. Thomas Schwenke</a></p>
        </div>
    </div>
</template>

<script>
export default {
methods: {
    goHome() {
    this.$router.push('/');
    }
}
}
</script>