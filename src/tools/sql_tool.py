"""
SQL tool — Parameterized patient cohort queries for the Oncology Care Insights Agent.
Connects to Azure SQL Database with Synthea/mCODE synthetic patient data.
Cancer types supported: breast | lung | colorectal
"""

import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Create a fresh connection to Azure SQL Database."""
    return pymssql.connect(
        server=os.getenv('AZURE_SQL_SERVER',
                         'oncology-sql-server.database.windows.net'),
        user='oncologyadmin',
        password=os.getenv('AZURE_SQL_PASSWORD'),
        database=os.getenv('AZURE_SQL_DATABASE', 'oncology-patients'),
        port=1433
    )

def get_cohort_stats(cancer_type: str = None) -> dict:
    """
    Returns count and basic stats for patients by cancer type.
    cancer_type: 'breast' | 'lung' | 'colorectal' | None (all types)
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if cancer_type:
            cursor.execute("""
                SELECT
                    c.cancer_type,
                    COUNT(DISTINCT c.patient_id) as patient_count,
                    SUM(CASE WHEN p.gender='female' THEN 1 ELSE 0 END) as female_count,
                    SUM(CASE WHEN p.gender='male' THEN 1 ELSE 0 END) as male_count
                FROM Conditions c
                JOIN Patients p ON c.patient_id = p.patient_id
                WHERE c.is_cancer = 1
                AND c.cancer_type = %s
                GROUP BY c.cancer_type
            """, (cancer_type,))
        else:
            cursor.execute("""
                SELECT
                    c.cancer_type,
                    COUNT(DISTINCT c.patient_id) as patient_count,
                    SUM(CASE WHEN p.gender='female' THEN 1 ELSE 0 END) as female_count,
                    SUM(CASE WHEN p.gender='male' THEN 1 ELSE 0 END) as male_count
                FROM Conditions c
                JOIN Patients p ON c.patient_id = p.patient_id
                WHERE c.is_cancer = 1
                AND c.cancer_type IS NOT NULL
                GROUP BY c.cancer_type
                ORDER BY patient_count DESC
            """)

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'cancer_type': row[0],
                'patient_count': row[1],
                'female_count': row[2],
                'male_count': row[3]
            })
        return {
            'status': 'success',
            'data': results,
            'note': 'All data is synthetic (Synthea/mCODE) — not real patients'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    finally:
        conn.close()


def get_treatment_distribution(cancer_type: str) -> dict:
    """
    Returns breakdown of top treatment regimens for a given cancer type.
    cancer_type: 'breast' | 'lung' | 'colorectal'
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT TOP 10
                t.treatment_text,
                t.treatment_type,
                COUNT(*) as count
            FROM Treatments t
            JOIN Conditions c ON t.patient_id = c.patient_id
            WHERE c.is_cancer = 1
            AND c.cancer_type = %s
            AND t.treatment_text IS NOT NULL
            AND t.treatment_text != ''
            GROUP BY t.treatment_text, t.treatment_type
            ORDER BY count DESC
        """, (cancer_type,))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'treatment': row[0],
                'type': row[1],
                'patient_count': row[2]
            })
        return {
            'status': 'success',
            'cancer_type': cancer_type,
            'data': results,
            'note': 'All data is synthetic (Synthea/mCODE) — not real patients'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    finally:
        conn.close()


def get_patient_panel_summary(cancer_type: str) -> dict:
    """
    Returns age distribution, gender split for a given cancer type.
    cancer_type: 'breast' | 'lung' | 'colorectal'
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Age distribution
        cursor.execute("""
            SELECT
                CASE
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 40
                        THEN 'Under 40'
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 50
                        THEN '40-49'
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 60
                        THEN '50-59'
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 70
                        THEN '60-69'
                    ELSE '70+'
                END as age_group,
                COUNT(DISTINCT p.patient_id) as count
            FROM Patients p
            JOIN Conditions c ON p.patient_id = c.patient_id
            WHERE c.is_cancer = 1
            AND c.cancer_type = %s
            GROUP BY
                CASE
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 40
                        THEN 'Under 40'
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 50
                        THEN '40-49'
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 60
                        THEN '50-59'
                    WHEN DATEDIFF(year, p.birth_date, GETDATE()) < 70
                        THEN '60-69'
                    ELSE '70+'
                END
            ORDER BY count DESC
        """, (cancer_type,))

        age_rows = cursor.fetchall()
        age_distribution = [
            {'age_group': row[0], 'count': row[1]}
            for row in age_rows
        ]

        # Gender split
        cursor.execute("""
            SELECT
                p.gender,
                COUNT(DISTINCT p.patient_id) as count
            FROM Patients p
            JOIN Conditions c ON p.patient_id = c.patient_id
            WHERE c.is_cancer = 1
            AND c.cancer_type = %s
            GROUP BY p.gender
        """, (cancer_type,))

        gender_rows = cursor.fetchall()
        gender_split = [
            {'gender': row[0], 'count': row[1]}
            for row in gender_rows
        ]

        return {
            'status': 'success',
            'cancer_type': cancer_type,
            'age_distribution': age_distribution,
            'gender_split': gender_split,
            'note': 'All data is synthetic (Synthea/mCODE) — not real patients'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    finally:
        conn.close()


if __name__ == "__main__":
    # Quick test
    print("Testing SQL tool functions...")
    print("\n📊 Cohort stats:")
    stats = get_cohort_stats()
    for item in stats['data']:
        print(f"  {item['cancer_type']}: {item['patient_count']} patients")

    print("\n👥 Breast cancer panel summary:")
    summary = get_patient_panel_summary('breast')
    for age in summary['age_distribution']:
        print(f"  {age['age_group']}: {age['count']} patients")

    print("\n✅ SQL tool ready!")
