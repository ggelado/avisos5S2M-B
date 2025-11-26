# Aclaración sobre el bucle infinito:

En el día de ayer hubo un pequeño bucle infinito en el código que gestiona el envío de notificaciones. Esto provocó que se lanzaran notificaciones de manera constante durante unos pocos minutos.

El motivo de este problema reside en la publicación de un aviso durante una modificación de la base de datos provocada por una suscripción.

## ¿Cómo funciona este sistema?

El sistema utilizado para mandar los avisos funciona del siguiente modo:

1. Leo el feed RSS
  
2. Compruebo si hay un post nuevo
  
3. De ser así abro la lista de subscriptores y les notifico
  

A priori parece sencillo, pero esto tiene una dificultad: Gestionar la lista de subscriptores y la lista de posts nuevos.

Como no tengo ningún servidor a mi disposición, he utilizado algunas herramientas gratuitas con sus limitaciones, y el sistema de base de datos se basa en Git y ficheros JSON.

## Detonante de la incidencia

En el día de ayer al mandar un aviso sobre la publicación de las notas de SSOO la máquina arrancó, parseó la lista de posts, hizo pull de la BD para asegurar la última versión, y comprobó que el post no estaba en el fichero `seen.json`. Entonces envió las notificaciones, actualizó el fichero dando el post como notificado, e hizo un push. En este tiempo entre el pull y el push, entró una modificación de una nueva subscripción, lo que provocó que la acción de push fallara:

```
Git pull stdout: 
Git pull stderr: From https://github.com/ggelado/notifierPushRSS
 * branch            main       -> FETCH_HEAD
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
Commit realizado: 
Commit realizado: 
Commit realizado: 
Commit realizado: 
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.Git pull stdout: 
Git pull stderr: From https://github.com/ggelado/notifierPushRSS
 * branch            main       -> FETCH_HEAD
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
Commit realizado: 
Commit realizado: 
Commit realizado: 
Commit realizado: 
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
Push fallido: To https://github.com/ggelado/notifierPushRSS.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'https://github.com/ggelado/notifierPushRSS.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

En cuanto se detectó que había un bucle infinito, se ordenó un paro inmediato de la máquina, hecho que tardó unos segundos en tramitarse, en los cuales se quedó en bucle infinito enviando notificaciones.

# Medidas tomadas

1. Para asegurar que no haya más incidencias a corto plazo se ha modificado el código que hacía push, forzando la introducción de cambios y evitando que se generen conflictos.
2. Entre parseo y parseo se establece una espera OBLIGATORIA de 300 segundos, lo que permitiría detectar y parar la máquina a tiempo en caso necesario.
3. UPDATE: Desde el 25 de noviembre se ha migrado el sistema a una base de datos que evite los errores y conflictos de la concurrencia, haciendo uso de un SGBD en condiciones.

### ¿Por qué no estaba ese código en un bloque con captura de excepciones?

Lo estaba, pero da lo mismo. La máquina está alojada en un servicio 0 downtime, por lo que si se lanza un error la máquina se reinicia sola, quiera o no, y al volver a encenderse, volvería a parsear los avisos y volvería a notificarlos, que es justo lo que pasó.

```javascript
execSync('shutdown now');
```

Esto sería lo más prudente pero mi hosting no me lo permite.

### ¿Podría haber una reversión automática?

Sí, pero en el momento que vuelve a un estado seguro, volvería a notificar.

### ¿Qué consecuencias puede tener este parche?

Existe el riesgo de que en caso de conflicto no se guarden subscripciones y algún usuario no sea notificado.

### ¿Por qué no se detectó antes?

Gran parte de los posts son automáticos, y están programados para lanzarse de madrugada, cuando hay menos tráfico (nulo).

## Medidas a tomar

No debería volver a suceder este error, pero se mantiene el estado BETA del servicio hasta futuras comprobaciones.
