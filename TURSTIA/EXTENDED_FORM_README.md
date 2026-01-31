# Formulaire Étendu de Crédit - Guide d'Utilisation

## Aperçu

Ce système combine **deux modèles d'évaluation de crédit** pour une décision optimale :

1. **Modèle ML** : Analyse les données structurées du formulaire
2. **Pipeline Qdrant/RAG** : Analyse documentaire et similarité vectorielle

## 🚀 Démarrage Rapide

### Backend
```bash
uvicorn backend.app:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run start
```

Accédez à : `http://localhost:4200/expanded-submission`

## 📋 Structure du Formulaire

Le formulaire de débriefing contient 10 sections :

| Section | Description |
|---------|-------------|
| 1️⃣ Métadonnées | Canal de contact, durée, agent |
| 2️⃣ Identification | Âge, statut client, ancienneté |
| 3️⃣ Situation Personnelle | État matrimonial, personnes à charge, conjoint |
| 4️⃣ Situation Professionnelle | Emploi, secteur, stabilité |
| 5️⃣ Situation Financière | Revenus, charges, dettes, épargne |
| 6️⃣ Demande de Crédit | Type, montant, durée, objet |
| 7️⃣ Indicateurs Comportementaux | Stress, urgence, clarté (échelles 1-5) |
| 8️⃣ Intention Réelle | Motivation, capacité de projection |
| 9️⃣ Risques Identifiés | Checklist de 6 facteurs de risque |
| 🔟 Synthèse | Profil de risque, capacité de remboursement |

## 🔄 Flux de Traitement

1. **Soumission** → Le formulaire est envoyé au backend
2. **Pipeline ML** → Extraction de 45+ features et prédiction
3. **Pipeline Qdrant** → Génération de résumé texte → embedding → recherche similarité
4. **Combinaison** → Les deux résultats sont combinés intelligemment
5. **Décision Finale** → ACCEPT, REJECT, ou MANUAL_REVIEW_REQUIRED

## 💡 Logique de Décision

```
Les deux modèles ACCEPTENT → Confiance élevée → ACCEPT
Les deux modèles REJETTENT → Confiance élevée → REJECT
Les modèles sont en désaccord → MANUAL_REVIEW_REQUIRED
Fraude détectée → FRAUD_STOP
Pas de cas similaires → COLD_START (ML prioritaire)
```

## 🤖 Modèle ML

### Mode Actuel : PLACEHOLDER

Le système fonctionne actuellement avec un modèle heuristique.

### Pour Ajouter Votre Modèle ML :

1. Placez le fichier modèle dans : `backend/models/credit_risk_model.pkl`
2. Le modèle doit être compatible scikit-learn
3. Interface attendue :
   ```python
   model.predict_proba(features_df)  # Retourne [[P(0), P(1)]]
   ```
4. Redémarrez le backend → Le modèle sera automatiquement chargé

## 📊 Résultat d'Évaluation

Le résultat combiné contient :

```json
{
  "final_decision": "ACCEPT",
  "reason": "BOTH_MODELS_AGREE_ACCEPT",
  "confidence": 0.72,
  "ml_assessment": {
    "ml_risk_score": 0.45,
    "ml_risk_level": "MEDIUM",
    "ml_prediction": "ACCEPT"
  },
  "qdrant_assessment": {
    "mode": "NORMAL",
    "final_decision": "ACCEPT",
    "confidence": 0.78
  }
}
```

## 🔍 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/submit-extended` | POST | Soumettre le formulaire étendu |
| `/api/submit-application` | POST | Soumettre le formulaire standard (existant) |

## 📁 Fichiers Clés

### Backend
- `backend/schemas/expanded_application.py` - Schéma Pydantic complet
- `backend/agents/ml_risk_agent.py` - Agent ML avec extraction de features
- `backend/services/extended_submission_service.py` - Orchestration des deux pipelines
- `backend/app.py` - Endpoint `/api/submit-extended`

### Frontend
- `frontend/src/app/features/submission/expanded-submission/` - Composant formulaire étendu
- `frontend/src/app/core/models/expanded-application.model.ts` - Modèles TypeScript

## ⚙️ Configuration

Aucune configuration supplémentaire requise. Le système utilise :
- Qdrant existant (config dans `backend/config.py`)
- Modèle d'embedding existant (sentence-transformers)
- Agents existants (fraud, risk, scenario, decision)

## 🧪 Tests

Pour tester le système :

1. Remplissez le formulaire avec des données variées
2. Cochez différents facteurs de risque
3. Testez avec/sans conjoint
4. Vérifiez les logs backend pour voir les deux pipelines s'exécuter
5. Examinez le résultat JSON pour voir la combinaison des évaluations

## 🎯 Cas d'Usage

✅ **Évaluation standard** : Les deux modèles s'accordent → décision rapide  
✅ **Cas complexe** : Désaccord → revue manuelle déclenchée  
✅ **Nouveau profil** : Pas de similarité → ML prend le relais  
✅ **Fraude suspectée** : Blocage automatique → investigation  

---

**Note** : Les erreurs TypeScript/Angular dans l'IDE sont normales si les dépendances npm ne sont pas installées. Exécutez `npm install` dans le dossier frontend pour les résoudre.
