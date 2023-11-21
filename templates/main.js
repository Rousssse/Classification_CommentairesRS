$(document).ready(function() {
    $("#submit-button").click(function() {
        // Récupérer les valeurs des radios
        var toxic = $("input[name='toxic']:checked").val();
        var obscene = $("input[name='obscene']:checked").val();
        var threatening = $("input[name='threatening']:checked").val();
        var insult = $("input[name='insult']:checked").val();

        // Envoyer les valeurs au serveur
        $.ajax({
            url: '/submit',
            type: 'POST',
            data: {
                'toxic': toxic,
                'obscene': obscene,
                'threatening': threatening,
                'insult': insult
            },
            success: function(response) {
                // Mettre à jour l'affichage avec les résultats
                $("#toxique").text(response.toxique ? 'Oui' : 'Non');
                $("#obscene").text(response.obscene ? 'Oui' : 'Non');
                $("#menace").text(response.menace ? 'Oui' : 'Non');
                $("#insulte").text(response.insulte ? 'Oui' : 'Non');

                $("#comment-row").html(response.comment_row_html);

                $("#toxic-result").text(response.toxic_result);
                $("#obscene-result").text(response.obscene_result);
                $("#threatening-result").text(response.threatening_result);
                $("#insult-result").text(response.insult_result);
            }
        });
    });
});