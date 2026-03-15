"""
Seed sample DORA documents for testing
"""
from models import init_db, get_session, Document, Topic, LegalLevel, DocumentType, BindingStatus, SourceBody
from datetime import datetime

def seed_sample_documents():
    """Add sample DORA documents to database"""
    engine = init_db()
    session = get_session(engine)
    
    # Get topics
    topics = session.query(Topic).all()
    topic_dict = {t.name: t for t in topics}
    
    # Sample documents
    sample_docs = [
        {
            'title': 'Regulation (EU) 2022/2554 - Digital Operational Resilience Act (DORA)',
            'summary': 'The main DORA regulation establishing uniform requirements for the security of network and information systems supporting the business processes of financial entities. It covers ICT risk management, incident reporting, digital operational resilience testing, ICT third-party risk management, and information sharing arrangements.',
            'full_text': 'This regulation lays down uniform requirements concerning the security of network and information systems supporting the business processes of financial entities. It applies to credit institutions, payment institutions, electronic money institutions, investment firms, crypto-asset service providers, central securities depositories, central counterparties, trading venues, trade repositories, managers of alternative investment funds, management companies, data reporting service providers, insurance and reinsurance undertakings, insurance intermediaries, reinsurance intermediaries, ancillary insurance intermediaries, institutions for occupational retirement provision, credit rating agencies, administrators of critical benchmarks, crowdfunding service providers, and securitisation repositories.',
            'legal_level': LegalLevel.LEVEL_1,
            'document_type': DocumentType.REGULATION,
            'binding_status': BindingStatus.BINDING,
            'source_body': SourceBody.EU_COMMISSION,
            'url': 'https://eur-lex.europa.eu/eli/reg/2022/2554/oj',
            'publication_date': datetime(2022, 12, 27),
            'applicability': 'All financial entities as defined in Article 2',
            'is_qa': False,
            'is_oversight_only': False,
            'topics': [topic_dict['ICT Risk Management'], topic_dict['ICT-Related Incidents']]
        },
        {
            'title': 'RTS on ICT Risk Management Framework',
            'summary': 'Regulatory Technical Standards specifying the detailed requirements for ICT risk management frameworks that financial entities must implement. Covers governance, risk identification, protection measures, detection capabilities, response and recovery procedures, and continuous improvement.',
            'full_text': 'These regulatory technical standards specify the components of the ICT risk management framework, including: governance and organization, ICT risk identification and assessment, ICT protection and prevention measures, ICT detection mechanisms, ICT response and recovery measures, learning and evolving capabilities, and communication. Financial entities shall maintain an ICT risk management framework that enables them to address ICT risk quickly, efficiently and comprehensively.',
            'legal_level': LegalLevel.LEVEL_2,
            'document_type': DocumentType.RTS,
            'binding_status': BindingStatus.TECHNICAL_STANDARD,
            'source_body': SourceBody.ESA_JOINT,
            'url': 'https://www.eiopa.europa.eu/document/download/example-rts-ict-risk',
            'publication_date': datetime(2024, 1, 17),
            'applicability': 'All financial entities subject to DORA',
            'is_qa': False,
            'is_oversight_only': False,
            'topics': [topic_dict['ICT Risk Management']]
        },
        {
            'title': 'RTS on ICT Incident Classification and Reporting',
            'summary': 'Technical standards defining criteria for classifying ICT-related incidents as major, including thresholds for impact on clients, financial impact, duration, geographical spread, data losses, criticality of services affected, and economic impact.',
            'full_text': 'This RTS establishes the criteria for determining whether an ICT-related incident is major and must be reported. Major incidents are those that meet specific thresholds related to: number of clients or financial counterparts affected, financial impact, duration of the incident, geographical spread, data losses, criticality of services affected, and economic impact. Financial entities must have processes to classify incidents and report major incidents to competent authorities.',
            'legal_level': LegalLevel.LEVEL_2,
            'document_type': DocumentType.RTS,
            'binding_status': BindingStatus.TECHNICAL_STANDARD,
            'source_body': SourceBody.ESA_JOINT,
            'url': 'https://www.eiopa.europa.eu/document/download/example-rts-incidents',
            'publication_date': datetime(2024, 1, 17),
            'applicability': 'All financial entities subject to DORA',
            'is_qa': False,
            'is_oversight_only': False,
            'topics': [topic_dict['ICT-Related Incidents']]
        },
        {
            'title': 'RTS on Threat-Led Penetration Testing (TLPT)',
            'summary': 'Regulatory Technical Standards on the requirements for threat-led penetration testing, including testing methodology, scope, frequency, testers qualifications, and reporting requirements. Applies to entities identified by competent authorities.',
            'full_text': 'These RTS specify the requirements for advanced testing of ICT tools, systems and processes through threat-led penetration testing (TLPT). The testing shall be performed by independent testers using intelligence on genuine threat actors and their tactics, techniques and procedures. Testing must cover people, processes and technologies. Results must be reported to senior management and competent authorities.',
            'legal_level': LegalLevel.LEVEL_2,
            'document_type': DocumentType.RTS,
            'binding_status': BindingStatus.TECHNICAL_STANDARD,
            'source_body': SourceBody.ESA_JOINT,
            'url': 'https://www.eiopa.europa.eu/document/download/example-rts-tlpt',
            'publication_date': datetime(2024, 1, 17),
            'applicability': 'Financial entities identified by competent authorities',
            'is_qa': False,
            'is_oversight_only': False,
            'topics': [topic_dict['Digital Operational Resilience Testing']]
        },
        {
            'title': 'RTS on ICT Third-Party Risk Management',
            'summary': 'Technical standards on the key elements of contractual arrangements between financial entities and ICT third-party service providers, including service level agreements, audit rights, termination rights, and subcontracting arrangements.',
            'full_text': 'This RTS specifies the minimum content of contractual arrangements with ICT third-party service providers. Contracts must include: detailed service descriptions, service levels and performance targets, locations where data will be processed, audit rights for the financial entity and competent authorities, termination rights, subcontracting arrangements, and business continuity requirements. Financial entities must maintain a register of all ICT third-party arrangements.',
            'legal_level': LegalLevel.LEVEL_2,
            'document_type': DocumentType.RTS,
            'binding_status': BindingStatus.TECHNICAL_STANDARD,
            'source_body': SourceBody.ESA_JOINT,
            'url': 'https://www.eiopa.europa.eu/document/download/example-rts-third-party',
            'publication_date': datetime(2024, 1, 17),
            'applicability': 'All financial entities using ICT third-party service providers',
            'is_qa': False,
            'is_oversight_only': False,
            'topics': [topic_dict['ICT Third-Party Risk Management']]
        },
        {
            'title': 'Guidelines on ICT Risk Management - Oversight Cooperation',
            'summary': 'Guidelines from ESAs on cooperation between competent authorities in the oversight of critical ICT third-party service providers (CTPPs). Covers information sharing, joint examinations, and coordination of supervisory actions.',
            'full_text': 'These guidelines establish the framework for cooperation between ESAs and national competent authorities in overseeing critical ICT third-party service providers. They cover: designation criteria for CTPPs, information sharing mechanisms, conduct of joint examinations, coordination of supervisory measures, and handling of cross-border issues. The guidelines aim to ensure consistent and effective oversight across the EU.',
            'legal_level': LegalLevel.LEVEL_3,
            'document_type': DocumentType.GUIDELINE,
            'binding_status': BindingStatus.GUIDANCE,
            'source_body': SourceBody.ESA_JOINT,
            'url': 'https://www.eiopa.europa.eu/document/download/example-guidelines-oversight',
            'publication_date': datetime(2024, 6, 15),
            'applicability': 'Competent authorities and ESAs',
            'is_qa': False,
            'is_oversight_only': True,
            'topics': [topic_dict['Oversight of Critical Third-Party Providers']]
        },
        {
            'title': 'Q&A: ICT Incident Reporting Timelines',
            'summary': 'Clarification on the timelines for reporting major ICT-related incidents. Initial notification must be submitted within 4 hours of classification, intermediate report within 72 hours, and final report within one month.',
            'full_text': 'Question: What are the exact timelines for reporting major ICT-related incidents under DORA? Answer: Financial entities must submit an initial notification to their competent authority within 4 hours of classifying an incident as major. An intermediate report providing updates must be submitted within 72 hours. A final report with root cause analysis and remediation measures must be submitted within one month of the initial notification. These timelines apply from the moment the incident is classified as major, not from when it first occurred.',
            'legal_level': LegalLevel.SUPPORTING,
            'document_type': DocumentType.QA,
            'binding_status': BindingStatus.INTERPRETIVE,
            'source_body': SourceBody.ESA_JOINT,
            'url': 'https://www.eiopa.europa.eu/qa/example-incident-timelines',
            'publication_date': datetime(2024, 9, 10),
            'applicability': 'All financial entities subject to incident reporting',
            'is_qa': True,
            'qa_status': 'FINAL',
            'is_oversight_only': False,
            'topics': [topic_dict['ICT-Related Incidents']]
        },
        {
            'title': 'Q&A: Subcontracting by ICT Third-Party Providers',
            'summary': 'Guidance on requirements when ICT third-party service providers subcontract critical or important functions. Financial entities must be notified and maintain oversight of subcontractors.',
            'full_text': 'Question: What are the requirements when an ICT third-party service provider wants to subcontract a critical or important function? Answer: The ICT third-party service provider must notify the financial entity before subcontracting. The financial entity must assess the subcontracting arrangement and can object if it poses risks. Contractual arrangements must include provisions on subcontracting, including the right to audit subcontractors. The financial entity remains responsible for compliance even when functions are subcontracted.',
            'legal_level': LegalLevel.SUPPORTING,
            'document_type': DocumentType.QA,
            'binding_status': BindingStatus.INTERPRETIVE,
            'source_body': SourceBody.EIOPA,
            'url': 'https://www.eiopa.europa.eu/qa/example-subcontracting',
            'publication_date': datetime(2024, 10, 5),
            'applicability': 'Financial entities using ICT third-party providers',
            'is_qa': True,
            'qa_status': 'FINAL',
            'is_oversight_only': False,
            'topics': [topic_dict['ICT Third-Party Risk Management']]
        }
    ]
    
    # Add documents to database
    for doc_data in sample_docs:
        topics = doc_data.pop('topics')
        doc = Document(**doc_data)
        doc.topics = topics
        session.add(doc)
    
    session.commit()
    print(f"✅ Successfully added {len(sample_docs)} sample DORA documents to database")
    
    # Show summary
    print("\nDocuments by type:")
    from sqlalchemy import func
    results = session.query(Document.document_type, func.count(Document.id)).group_by(Document.document_type).all()
    for doc_type, count in results:
        print(f"  {doc_type.value}: {count}")
    
    session.close()

if __name__ == "__main__":
    seed_sample_documents()

# Made with Bob
