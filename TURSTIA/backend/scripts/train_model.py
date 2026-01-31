"""
ML Model Training Script
Trains a credit risk prediction model using synthetic data
"""
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(data_path: Path) -> pd.DataFrame:
    """Load the synthetic credit dataset."""
    print(f"📂 Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def prepare_features(df: pd.DataFrame):
    """Separate features and target."""
    # Target variable
    y = df['default'].values
    
    # Features (all except target)
    X = df.drop('default', axis=1).values
    feature_names = df.drop('default', axis=1).columns.tolist()
    
    return X, y, feature_names


def train_model(X_train, y_train, model_type='random_forest'):
    """Train the ML model."""
    print(f"\n🤖 Training {model_type} model...")
    
    if model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
    elif model_type == 'gradient_boosting':
        model = GradientBoostingClassifier(
            n_estimators=150,
            max_depth=8,
            learning_rate=0.1,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    print(f"   ✅ Model trained successfully")
    
    return model


def evaluate_model(model, X_test, y_test, feature_names):
    """Evaluate model performance."""
    print("\n📊 Evaluating model performance...")
    
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(y_test, y_pred, target_names=['No Default', 'Default']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(f"                 Predicted")
    print(f"                 No  Yes")
    print(f"Actual No     {cm[0,0]:5d} {cm[0,1]:5d}")
    print(f"       Yes    {cm[1,0]:5d} {cm[1,1]:5d}")
    
    # ROC AUC
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\n🎯 ROC AUC Score: {roc_auc:.4f}")
    
    # Feature Importance
    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🔝 Top 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))
    
    return {
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }


def save_model(model, output_path: Path):
    """Save the trained model to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\n💾 Model saved to: {output_path}")
    print(f"   Model size: {output_path.stat().st_size / 1024:.1f} KB")


def plot_feature_importance(model, feature_names, output_dir: Path):
    """Plot feature importance."""
    if not hasattr(model, 'feature_importances_'):
        return
    
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False).head(15)
    
    plt.figure(figsize=(10, 8))
    plt.barh(range(len(feature_importance)), feature_importance['importance'].values)
    plt.yticks(range(len(feature_importance)), feature_importance['feature'].values)
    plt.xlabel('Importance')
    plt.title('Top 15 Feature Importances')
    plt.tight_layout()
    
    plot_path = output_dir / 'feature_importance.png'
    plt.savefig(plot_path, dpi=100, bbox_inches='tight')
    print(f"\n📈 Feature importance plot saved to: {plot_path}")
    plt.close()


def main():
    """Main training pipeline."""
    print("="*60)
    print("ML MODEL TRAINING PIPELINE")
    print("="*60)
    
    # Paths
    script_dir = Path(__file__).parent
    backend_dir = script_dir.parent
    data_dir = backend_dir / "data"
    models_dir = backend_dir / "models"
    
    data_path = data_dir / "synthetic_credit_data.csv"
    model_path = models_dir / "credit_risk_model.pkl"
    
    # Check if data exists
    if not data_path.exists():
        print(f"\n❌ Data file not found: {data_path}")
        print("   Please run generate_synthetic_data.py first!")
        return
    
    # Load data
    df = load_data(data_path)
    
    # Prepare features
    X, y, feature_names = prepare_features(df)
    print(f"\n📋 Dataset info:")
    print(f"   Total samples: {len(X)}")
    print(f"   Features: {len(feature_names)}")
    print(f"   Default rate: {y.mean():.2%}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n✂️ Train/test split:")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train model
    model = train_model(X_train, y_train, model_type='random_forest')
    
    # Evaluate model
    results = evaluate_model(model, X_test, y_test, feature_names)
    
    # Save model
    save_model(model, model_path)
    
    # Plot feature importance
    plot_feature_importance(model, feature_names, models_dir)
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📦 Model ready for deployment at:")
    print(f"   {model_path}")
    print(f"\n🎯 Model Performance Summary:")
    print(f"   ROC AUC Score: {results['roc_auc']:.4f}")
    print(f"   Training accuracy: {model.score(X_train, y_train):.2%}")
    print(f"   Testing accuracy: {model.score(X_test, y_test):.2%}")


if __name__ == "__main__":
    main()
